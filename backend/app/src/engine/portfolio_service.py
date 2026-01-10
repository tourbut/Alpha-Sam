"""
포트폴리오 수익률 계산 서비스
domain_rules.md의 계산 규칙을 정확히 따름
"""
from typing import Optional, List, Dict
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.portfolio import Portfolio
from app.src.models.position import Position
from app.src.models.transaction import Transaction
from app.src.models.asset import Asset


def calculate_position_metrics(
    quantity: float,
    buy_price: float,
    current_price: Optional[float]
) -> Dict[str, Optional[float]]:
    """
    단일 포지션의 평가액, 손익, 수익률 계산
    
    Args:
        quantity: 보유 수량
        buy_price: 매수 단가
        current_price: 현재 가격 (None이면 계산 불가)
    
    Returns:
        {
            "valuation": 평가액 (current_price * quantity),
            "profit_loss": 손익 ((current_price - buy_price) * quantity),
            "return_rate": 수익률 (((current_price - buy_price) / buy_price) * 100)
        }
        current_price가 None이면 모든 값이 None
    """
    if current_price is None:
        return {
            "valuation": None,
            "profit_loss": None,
            "return_rate": None
        }
    
    # 0으로 나누기 방지
    if buy_price <= 0:
        return {
            "valuation": None,
            "profit_loss": None,
            "return_rate": None
        }
    
    # 평가액 = current_price * quantity
    valuation = current_price * quantity
    
    # 손익 = (current_price - buy_price) * quantity
    profit_loss = (current_price - buy_price) * quantity
    
    # 수익률 = ((current_price - buy_price) / buy_price) * 100
    return_rate = ((current_price - buy_price) / buy_price) * 100
    
    return {
        "valuation": round(valuation, 2),
        "profit_loss": round(profit_loss, 2),
        "return_rate": round(return_rate, 2)
    }


def calculate_portfolio_summary(
    positions: List[Dict[str, float]]
) -> Dict[str, Optional[float]]:
    """
    전체 포트폴리오의 총 평가액, 총 손익, 포트폴리오 수익률 계산
    
    Args:
        positions: 포지션 리스트, 각 포지션은 다음 키를 가짐:
            - "quantity": 보유 수량
            - "buy_price": 매수 단가
            - "current_price": 현재 가격 (Optional)
    
    Returns:
        {
            "total_valuation": 총 평가액,
            "total_profit_loss": 총 손익,
            "total_invested": 총 투자 원금,
            "portfolio_return_rate": 포트폴리오 수익률 (원금 가중)
        }
    """
    total_valuation = Decimal("0")
    total_profit_loss = Decimal("0")
    total_invested = Decimal("0")
    
    for position in positions:
        quantity = Decimal(str(position.get("quantity", 0)))
        buy_price = Decimal(str(position.get("buy_price", 0)))
        current_price = position.get("current_price")
        
        # 총 투자 원금 계산
        invested = buy_price * quantity
        total_invested += invested
        
        if current_price is not None and buy_price > 0:
            current_price_decimal = Decimal(str(current_price))
            
            # 총 평가액 계산
            valuation = current_price_decimal * quantity
            total_valuation += valuation
            
            # 총 손익 계산
            profit_loss = (current_price_decimal - buy_price) * quantity
            total_profit_loss += profit_loss
    
    # 포트폴리오 수익률 계산 (원금 가중 수익률)
    # portfolio_return_rate = ((total_valuation - total_invested) / total_invested) * 100
    portfolio_return_rate = None
    if total_invested > 0:
        portfolio_return_rate = float(
            ((total_valuation - total_invested) / total_invested) * Decimal("100")
        )
        portfolio_return_rate = round(portfolio_return_rate, 2)
    
    return {
        "total_valuation": float(total_valuation) if total_valuation > 0 else None,
        "total_profit_loss": float(total_profit_loss),
        "total_invested": float(total_invested) if total_invested > 0 else None,
        "portfolio_return_rate": portfolio_return_rate
    }


class PortfolioService:
    async def create_portfolio(self, session: AsyncSession, owner_id: int, name: str, description: str = None) -> Portfolio:
        portfolio = Portfolio(owner_id=owner_id, name=name, description=description)
        session.add(portfolio)
        await session.commit()
        await session.refresh(portfolio)
        return portfolio

    async def get_user_portfolios(self, session: AsyncSession, owner_id: int) -> List[Portfolio]:
        stmt = select(Portfolio).where(Portfolio.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_portfolio(self, session: AsyncSession, portfolio_id: int, owner_id: int) -> Optional[Portfolio]:
        stmt = select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_portfolio_positions(self, session: AsyncSession, portfolio_id: int) -> List[Position]:
        stmt = select(Position).where(Position.portfolio_id == portfolio_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def add_transaction(self, session: AsyncSession, portfolio_id: int, asset_id: int, type: str, quantity: float, price: float, executed_at) -> Transaction:
        # 1. Add Transaction
        tx = Transaction(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            type=type,
            quantity=quantity,
            price=price,
            executed_at=executed_at
        )
        session.add(tx)
        await session.flush() # get ID

        # 2. Re-calculate Position
        await self._recalculate_position(session, portfolio_id, asset_id)
        
        await session.commit()
        await session.refresh(tx)
        return tx

    async def _recalculate_position(self, session: AsyncSession, portfolio_id: int, asset_id: int):
        # Fetch all transactions for this asset in this portfolio, ordered by time
        stmt = select(Transaction).where(
            Transaction.portfolio_id == portfolio_id,
            Transaction.asset_id == asset_id
        ).order_by(Transaction.executed_at, Transaction.id)
        
        result = await session.execute(stmt)
        transactions = result.scalars().all()
        
        current_qty = Decimal("0")
        total_cost = Decimal("0") # for avg price calc
        
        # Simple Weighted Average Price Calculation
        for tx in transactions:
            qty = Decimal(str(tx.quantity))
            price = Decimal(str(tx.price))
            
            if tx.type == "BUY":
                current_qty += qty
                total_cost += (qty * price)
            elif tx.type == "SELL":
                # For SELL, we reduce quantity. Avg price doesn't change usually, but realized PnL happens.
                # However, we need to maintain total_cost proportional to remaining qty to keep Avg Price same.
                if current_qty > 0:
                    avg_price = total_cost / current_qty
                    current_qty -= qty
                    # New total cost matches the remaining qty * avg_price
                    total_cost = current_qty * avg_price
                else:
                    # Selling from 0 or negative (shouldn't happen with constraints)
                    current_qty -= qty
            
            if current_qty < 0:
                 # Logic for short selling? For now assume long-only.
                 current_qty = Decimal("0")
                 total_cost = Decimal("0")

        # Update or Create Position
        avg_price = (total_cost / current_qty) if current_qty > 0 else Decimal("0")
        
        # Check existing position
        stmt_pos = select(Position).where(
            Position.portfolio_id == portfolio_id,
            Position.asset_id == asset_id
        )
        result_pos = await session.execute(stmt_pos)
        position = result_pos.scalar_one_or_none()
        
        if position:
            position.quantity = float(current_qty)
            position.avg_price = float(avg_price)
            if transactions:
                position.last_transaction_id = transactions[-1].id
        else:
            position = Position(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                quantity=float(current_qty),
                avg_price=float(avg_price),
                last_transaction_id=transactions[-1].id if transactions else None
            )
            session.add(position)

portfolio_service_instance = PortfolioService()
