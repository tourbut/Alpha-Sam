from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.src.models.transaction import Transaction
from app.src.models.position import Position
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.schemas.transaction import TransactionCreate # Schema가 있다고 가정

class TransactionService:
    @staticmethod
    async def create_transaction(session: AsyncSession, transaction_data: dict) -> Transaction:
        """
        Transaction 생성 및 Position Atomic Update (Hybrid Approach)
        """
        portfolio_id = transaction_data.get("portfolio_id")
        asset_id = transaction_data.get("asset_id")
        tx_type = transaction_data.get("type") # 'BUY' or 'SELL'
        quantity = float(transaction_data.get("quantity"))
        price = float(transaction_data.get("price"))
        
        # 0. Validate Portfolio Ownership (Optional check if not done in dependency)
        # 여기서는 생략, API 레벨에서 체크한다고 가정

        # 1. Start Atomic Block (Implicit in SQLAlchemy AsyncSession with commit at end)
        
        # 1-1. Create Transaction Record
        new_tx = Transaction(**transaction_data)
        session.add(new_tx)
        
        # 1-2. Get Position with Lock (For Update) to prevent race condition
        # PostgreSQL: FOR UPDATE
        stmt = (
            select(Position)
            .where(Position.portfolio_id == portfolio_id)
            .where(Position.asset_id == asset_id)
            .with_for_update()
        )
        result = await session.execute(stmt)
        position = result.scalar_one_or_none()
        
        if not position:
            if tx_type == 'SELL':
                # 없는 포지션을 매도할 수는 없음 (공매도 미지원 가정)
                raise HTTPException(status_code=400, detail="Cannot sell asset not owned (No position found).")
            
            # Create new Position
            position = Position(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                quantity=0,
                avg_price=0
            )
            session.add(position)
            # Flush to get ID if needed, but not strictly necessary here
        
        # 1-3. Update Position Logic
        if tx_type == 'BUY':
            # Calculate New Avg Price (Moving Average)
            total_value = (position.quantity * position.avg_price) + (quantity * price)
            total_quantity = position.quantity + quantity
            
            if total_quantity > 0:
                position.avg_price = total_value / total_quantity
            else:
                position.avg_price = 0 # Should not happen defined by logic
                
            position.quantity = total_quantity
            
        elif tx_type == 'SELL':
            if position.quantity < quantity:
                raise HTTPException(status_code=400, detail="Insufficient quantity to sell.")
            
            # 매도 시 평단가는 변하지 않음 (이익 실현)
            position.quantity -= quantity
            
            # 수량이 0이 되면 포지션을 남겨둘지 삭제할지 결정. 
            # 이력 관리를 위해 남겨두되(0), 조회 시 필터링하는 것이 일반적.
            # 하지만 0.00000001 같은 Dust가 남을 수 있으므로 주의.
        
        # Position is already attached to session
        
        # 2. Commit and Refresh
        await session.commit()
        await session.refresh(new_tx)
        return new_tx

    @staticmethod
    async def get_portfolio_positions(session: AsyncSession, portfolio_id: int):
        """
        포지션 목록 조회 (Snapshot 기반 O(1))
        """
        stmt = (
            select(Position)
            .where(Position.portfolio_id == portfolio_id)
            .where(Position.quantity > 0) # 0인 포지션 제외
            .options(selectinload(Position.asset))
        )
        result = await session.execute(stmt)
        return result.scalars().all()
