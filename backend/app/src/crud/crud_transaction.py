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
from fastapi import HTTPException, status

async def create_transaction(*, session: AsyncSession, transaction_in: TransactionCreate, owner_id: int) -> Transaction:
    """
    거래 생성 및 포지션 업데이트 (Atomic)
    1. Transaction 레코드 생성
    2. Position 레코드 업데이트 (없으면 생성)
       - BUY: 수량 증가, 평단가 재계산 (이동평균법)
       - SELL: 수량 감소, 실현 손익 계산 (선입선출법 가정은 복잡하므로 일단 단순 평단가 유지 후 수량 차감 방식 적용)
         * 기획상 SELL 시 평단가는 변하지 않고 수량만 줄어듦. (이동평균법의 일반적 규칙)
    """
    try:
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
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Cannot sell asset without an existing position"
                )
                
            # First purchase: Create new position
            position = Position(
                asset_id=transaction_in.asset_id,
                owner_id=owner_id,
                quantity=transaction_in.quantity,
                buy_price=transaction_in.price,
                buy_date=func.current_date()
            )
            session.add(position)
            
        else:
            # Update existing position using Weighted Average Cost method
            current_qty = float(position.quantity)
            current_avg_price = float(position.buy_price)
            
            if transaction_in.type == "BUY":
                # BUY: Increase quantity and recalculate average price
                new_qty = current_qty + transaction_in.quantity
                if new_qty > 0:
                    total_cost = (current_qty * current_avg_price) + (transaction_in.quantity * transaction_in.price)
                    new_avg_price = total_cost / new_qty
                    position.buy_price = new_avg_price
                
                position.quantity = new_qty
                
            elif transaction_in.type == "SELL":
                # SELL: Decrease quantity, keep average price
                if current_qty < transaction_in.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail=f"Insufficient quantity. Owned: {current_qty}, Requested: {transaction_in.quantity}"
                    )
                
                new_qty = current_qty - transaction_in.quantity
                position.quantity = new_qty
                
                # If quantity reaches zero, we could delete the position, but keeping it at 0 
                # might be easier for history tracking. However, most users prefer it gone.
                # For now, we keep it as 0 to avoid breaking potential foreign keys if any.
                
        await session.commit()
        await session.refresh(db_transaction)
        return db_transaction
    except HTTPException as he:
        # HTTP Exception은 그대로 전파 (이미 로직적 에러임)
        await session.rollback()
        raise he
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def get_transactions(
    *, 
    session: AsyncSession, 
    owner_id: int,
    skip: int = 0, 
    limit: int = 100,
    asset_id: Optional[int] = None
) -> List[Transaction]:
    """
    거래 내역 조회 (Owner 본인 것만)
    """
    try:
        stmt = select(Transaction).where(Transaction.owner_id == owner_id)
        
        if asset_id:
            stmt = stmt.where(Transaction.asset_id == asset_id)
            
        stmt = stmt.order_by(desc(Transaction.timestamp)).offset(skip).limit(limit)
        
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(e)
        raise e
