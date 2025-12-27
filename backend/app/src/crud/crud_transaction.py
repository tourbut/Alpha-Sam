"""
Transaction CRUD Module
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.src.models.transaction import Transaction
from app.src.schemas.transaction import TransactionCreate
from app.src.models.position import Position
from app.src.models.asset import Asset
from fastapi import HTTPException

async def create_transaction(session: AsyncSession, transaction_in: TransactionCreate, owner_id: int) -> Transaction:
    """
    거래 생성 및 포지션 업데이트 (Atomic)
    1. Transaction 레코드 생성
    2. Position 레코드 업데이트 (없으면 생성)
       - BUY: 수량 증가, 평단가 재계산 (이동평균법)
       - SELL: 수량 감소, 실현 손익 계산 (선입선출법 가정은 복잡하므로 일단 단순 평단가 유지 후 수량 차감 방식 적용)
         * 기획상 SELL 시 평단가는 변하지 않고 수량만 줄어듦. (이동평균법의 일반적 규칙)
    """
    # 1. 자산 존재 확인
    asset = await session.get(Asset, transaction_in.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # 2. Transaction 생성
    db_transaction = Transaction(
        asset_id=transaction_in.asset_id,
        owner_id=owner_id,
        type=transaction_in.type,
        quantity=transaction_in.quantity,
        price=transaction_in.price,
        # total_amount=transaction_in.quantity * transaction_in.price # DB 컬럼 제거함
        timestamp=func.now()
    )
    session.add(db_transaction)
    
    # 3. Position 조회 또는 생성
    # [Multi-tenancy] owner_id 필터 추가
    stmt = select(Position).where(
        Position.asset_id == transaction_in.asset_id,
        Position.owner_id == owner_id
    )
    result = await session.execute(stmt)
    position = result.scalar_one_or_none()
    
    if not position:
        if transaction_in.type == "SELL":
            raise HTTPException(status_code=400, detail="Cannot sell asset without position")
            
        # 첫 매수: 새 포지션 생성
        position = Position(
            asset_id=transaction_in.asset_id,
            owner_id=owner_id,
            quantity=transaction_in.quantity,
            buy_price=transaction_in.price,
            buy_date=func.current_date() # 오늘 날짜
        )
        session.add(position)
        
    else:
        # 기존 포지션 업데이트
        current_qty = float(position.quantity)
        current_avg_price = float(position.buy_price)
        
        if transaction_in.type == "BUY":
            # 매수: 수량 증가, 평단가 재계산
            # New Price = ((Old Qty * Old Price) + (New Qty * New Price)) / (Old Qty + New Qty)
            new_qty = current_qty + transaction_in.quantity
            total_cost = (current_qty * current_avg_price) + (transaction_in.quantity * transaction_in.price)
            new_avg_price = total_cost / new_qty
            
            position.quantity = new_qty
            position.buy_price = new_avg_price
            
        elif transaction_in.type == "SELL":
            # 매도: 수량 감소, 평단가 유지
            if current_qty < transaction_in.quantity:
                raise HTTPException(status_code=400, detail="Insufficient quantity to sell")
            
            new_qty = current_qty - transaction_in.quantity
            position.quantity = new_qty
            
            # 전량 매도 시 포지션을 삭제할지 0으로 남길지 결정 필요.
            # 0으로 남기면 평단가 정보가 남아 재진입 시 왜곡될 수 있으나, 0이면 평단가 의미 없음.
            # 여기서는 0이 되면 포지션 삭제 로직을 추가할 수도 있음.
            # 일단 0으로 유지.
            
    await session.commit()
    await session.refresh(db_transaction)
    return db_transaction

async def get_transactions(
    session: AsyncSession, 
    owner_id: int,
    skip: int = 0, 
    limit: int = 100,
    asset_id: Optional[int] = None
) -> List[Transaction]:
    """
    거래 내역 조회 (Owner 본인 것만)
    """
    stmt = select(Transaction).where(Transaction.owner_id == owner_id)
    
    if asset_id:
        stmt = stmt.where(Transaction.asset_id == asset_id)
        
    stmt = stmt.order_by(desc(Transaction.timestamp)).offset(skip).limit(limit)
    
    result = await session.execute(stmt)
    return result.scalars().all()
