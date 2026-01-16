"""
Transaction CRUD Module
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.src.models.transaction import Transaction
from app.src.models.portfolio import Portfolio
from app.src.schemas.transaction import TransactionCreate
from app.src.models.asset import Asset
from fastapi import HTTPException


async def create_transaction(*, session: AsyncSession, transaction_in: TransactionCreate, owner_id: int) -> Transaction:
    """
    거래 생성 (단순화)
    1. 사용자의 Portfolio를 찾아서 Transaction 레코드 생성
    참고: Position은 더 이상 DB에 저장하지 않고, 필요 시 Transaction을 집계하여 계산함
    """
    try:
        # 1. 자산 존재 확인
        asset = await session.get(Asset, transaction_in.asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # 2. 사용자의 Portfolio 조회 (첫 번째 포트폴리오 사용)
        portfolio_stmt = select(Portfolio).where(Portfolio.owner_id == owner_id).limit(1)
        portfolio_result = await session.execute(portfolio_stmt)
        portfolio = portfolio_result.scalar_one_or_none()
        
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found for user")
            
        # 3. Transaction 생성
        db_transaction = Transaction(
            portfolio_id=portfolio.id,
            asset_id=transaction_in.asset_id,
            type=transaction_in.type,
            quantity=transaction_in.quantity,
            price=transaction_in.price,
        )
        session.add(db_transaction)
        
        await session.commit()
        await session.refresh(db_transaction)
        return db_transaction
    except HTTPException as he:
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
    거래 내역 조회 (Owner의 Portfolio에 속한 Transaction만)
    """
    try:
        # 사용자의 Portfolio ID 목록 조회
        portfolio_stmt = select(Portfolio.id).where(Portfolio.owner_id == owner_id)
        portfolio_result = await session.execute(portfolio_stmt)
        portfolio_ids = portfolio_result.scalars().all()
        
        if not portfolio_ids:
            return []
        
        # Transaction 조회 (Portfolio ID 기반)
        stmt = select(Transaction).where(Transaction.portfolio_id.in_(portfolio_ids))
        
        if asset_id:
            stmt = stmt.where(Transaction.asset_id == asset_id)
            
        stmt = stmt.order_by(desc(Transaction.executed_at)).offset(skip).limit(limit)
        
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(e)
        raise e
