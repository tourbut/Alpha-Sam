"""
Transaction CRUD Module
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.src.models.transaction import Transaction
from app.src.schemas.transaction import TransactionCreate
from app.src.models.asset import Asset
from fastapi import HTTPException, status

async def create_transaction(*, session: AsyncSession, transaction_in: TransactionCreate, owner_id: int) -> Transaction:
    """
    거래 생성 (단순화)
    1. Transaction 레코드 생성
    참고: Position은 더 이상 DB에 저장하지 않고, 필요 시 Transaction을 집계하여 계산함
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
            timestamp=func.now()
        )
        session.add(db_transaction)
        
        # Position 업데이트 로직 제거됨
        # (더 이상 필요 없음, Transaction 기반으로 실시간 계산)
        
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
