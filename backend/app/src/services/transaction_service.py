from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.src.models.transaction import Transaction
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.schemas.transaction import TransactionCreate # Schema가 있다고 가정
import uuid

class TransactionService:
    @staticmethod
    async def create_transaction(session: AsyncSession, transaction_data: dict) -> Transaction:
        """
        Transaction 생성만 수행. 
        Position 정보는 자산 및 거래 내역을 통해 런타임에 동적으로 계산되므로 DB 상태 저장 불필요
        """
        portfolio_id = transaction_data.get("portfolio_id")
        asset_id = transaction_data.get("asset_id")
        tx_type = transaction_data.get("type") # 'BUY' or 'SELL'
        quantity = Decimal(str(transaction_data.get("quantity")))
        
        # 1-1. Create Transaction Record
        new_tx = Transaction(**transaction_data)
        session.add(new_tx)

        if tx_type == 'SELL':
            # 매도시 잔고 부족 여부 검증
            from app.src.services.portfolio_service import PortfolioService
            positions, _ = await PortfolioService._get_portfolio_core_data(session, portfolio_id)
            position = next((p for p in positions if p.asset_id == asset_id), None)
            
            if not position:
                raise HTTPException(status_code=400, detail="Cannot sell asset not owned (No position found).")
            
            current_quantity = Decimal(str(position.quantity))
            if current_quantity < quantity:
                raise HTTPException(status_code=400, detail="Insufficient quantity to sell.")

        # 2. Commit and Refresh
        await session.commit()
        await session.refresh(new_tx)
        return new_tx

    @staticmethod
    async def get_portfolio_positions(session: AsyncSession, portfolio_id: uuid.UUID):
        """
        포지션 목록 조회 (Computed)
        """
        from app.src.services.portfolio_service import PortfolioService
        return await PortfolioService.get_positions(session, portfolio_id)
