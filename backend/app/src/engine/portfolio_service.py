"""
포트폴리오 수익률 계산 서비스
domain_rules.md의 계산 규칙을 정확히 따름
"""
import uuid
from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.src.models.portfolio import Portfolio
from app.src.models.transaction import Transaction
from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.schemas.position import PositionWithAsset


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


async def calculate_positions_from_transactions(
    session: AsyncSession,
    portfolio_id: uuid.UUID
) -> List[PositionWithAsset]:
    """
    Portfolio의 모든 Transaction을 Asset별로 집계하여 Position 계산
    
    Args:
        session: Database session
        portfolio_id: Portfolio ID
    
    Returns:
        PositionWithAsset 리스트 (asset 정보 포함)
    """
    # 1. 해당 Portfolio의 모든 Transaction 조회 (Asset join)
    stmt = (
        select(Transaction)
        .where(Transaction.portfolio_id == portfolio_id)
        .options(selectinload(Transaction.asset))
        .order_by(Transaction.executed_at, Transaction.id)
    )
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    
    if not transactions:
        return []
    
    # 2. Asset별로 Transaction 그룹화
    asset_transactions: Dict[int, List[Transaction]] = {}
    for tx in transactions:
        if tx.asset_id not in asset_transactions:
            asset_transactions[tx.asset_id] = []
        asset_transactions[tx.asset_id].append(tx)
    
    # 3. 각 Asset별로 Position 계산
    positions: List[PositionWithAsset] = []
    
    for asset_id, txs in asset_transactions.items():
        current_qty = Decimal("0")
        total_cost = Decimal("0")  # for avg price calc
        
        # Weighted Average Price 계산
        for tx in txs:
            qty = Decimal(str(tx.quantity))
            price = Decimal(str(tx.price))
            
            if tx.type == "BUY":
                current_qty += qty
                total_cost += (qty * price)
            elif tx.type == "SELL":
                # SELL: 수량 감소, 평단가 유지
                if current_qty > 0:
                    avg_price = total_cost / current_qty
                    current_qty -= qty
                    # 남은 수량에 대한 total_cost 재계산
                    total_cost = current_qty * avg_price
                else:
                    # 보유 수량이 없는데 SELL (이론적으로는 검증에서 걸러져야 함)
                    current_qty -= qty
            
            # 음수 수량 방지
            if current_qty < 0:
                current_qty = Decimal("0")
                total_cost = Decimal("0")
        
        # 최종 평단가 계산
        avg_price = (total_cost / current_qty) if current_qty > 0 else Decimal("0")
        
        # 수량이 0보다 큰 경우만 Position으로 추가
        if current_qty > 0:
            # Asset 정보 가져오기 (이미 selectinload로 로드됨)
            asset = txs[0].asset
            
            # 최신 가격 조회 (선택 사항, 여기서는 일단 None)
            # 나중에 Price 조회 로직 추가 가능
            
            position = PositionWithAsset(
                id=None,  # DB ID 없음
                asset_id=asset_id,
                quantity=float(current_qty),
                avg_price=float(avg_price),
                created_at=None,
                updated_at=None,
                # Asset 정보
                asset_symbol=asset.symbol if asset else None,
                asset_name=asset.name if asset else None,
                asset_category=asset.category if asset else None,
                # 계산된 필드는 나중에 추가
                valuation=None,
                profit_loss=None,
                return_rate=None,
                current_price=None
            )
            positions.append(position)
    
    return positions


class PortfolioService:
    async def create_portfolio(self, session: AsyncSession, owner_id: uuid.UUID, name: str, description: Optional[str] = None) -> Portfolio:
        portfolio = Portfolio(owner_id=owner_id, name=name, description=description)
        session.add(portfolio)
        await session.commit()
        await session.refresh(portfolio)
        return portfolio

    async def get_user_portfolios(self, session: AsyncSession, owner_id: uuid.UUID) -> List[Portfolio]:
        stmt = select(Portfolio).where(Portfolio.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_portfolio(self, session: AsyncSession, portfolio_id: uuid.UUID, owner_id: uuid.UUID) -> Optional[Portfolio]:
        stmt = select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_portfolio_positions(self, session: AsyncSession, portfolio_id: uuid.UUID) -> List[PositionWithAsset]:
        """Portfolio의 Position 목록 조회 (Transaction 기반 계산)"""
        return await calculate_positions_from_transactions(session, portfolio_id)

    async def add_transaction(
        self, 
        session: AsyncSession, 
        portfolio_id: uuid.UUID, 
        asset_id: uuid.UUID, 
        type: str, quantity: float, price: float, executed_at) -> Transaction:
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
        
        # 2. Position 재계산 로직 제거 (더 이상 필요 없음)
        # await self._recalculate_position(session, portfolio_id, asset_id)
        
        await session.commit()
        await session.refresh(tx)
        return tx

portfolio_service_instance = PortfolioService()
