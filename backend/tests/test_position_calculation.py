"""
Position Calculation Test
Transaction 기반 Position 계산 로직 테스트
"""
import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.engine.portfolio_service import calculate_positions_from_transactions
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction
from app.src.models.user import User
from datetime import datetime


@pytest.mark.asyncio
async def test_no_transactions_returns_empty_list(async_session: AsyncSession):
    """Transaction이 없으면 빈 리스트 반환"""
    # Setup: User, Portfolio, Asset 생성
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Test Portfolio")
    async_session.add(portfolio)
    await async_session.commit()
    
    # Execute
    positions = await calculate_positions_from_transactions(async_session, portfolio.id)
    
    # Assert
    assert positions == []


@pytest.mark.asyncio
async def test_buy_only_transactions(async_session: AsyncSession):
    """BUY만 있는 경우 수량, 평단가 계산 정확성 검증"""
    # Setup
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Test Portfolio")
    async_session.add(portfolio)
    await async_session.flush()
    
    asset = Asset(symbol="BTC", name="Bitcoin", category="Crypto")
    async_session.add(asset)
    await async_session.flush()
    
    # Transaction 1: BUY 10 @ $100
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=10.0,
        price=100.0,
        executed_at=datetime(2026, 1, 1, 10, 0, 0)
    )
    async_session.add(tx1)
    
    # Transaction 2: BUY 5 @ $120
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=5.0,
        price=120.0,
        executed_at=datetime(2026, 1, 2, 10, 0, 0)
    )
    async_session.add(tx2)
    await async_session.commit()
    
    # Execute
    positions = await calculate_positions_from_transactions(async_session, portfolio.id)
    
    # Assert
    assert len(positions) == 1
    pos = positions[0]
    assert pos.asset_id == asset.id
    assert pos.quantity == 15.0  # 10 + 5
    # 평단가 = (10*100 + 5*120) / 15 = 1600 / 15 = 106.67
    assert abs(pos.avg_price - 106.67) < 0.01
    assert pos.asset_symbol == "BTC"


@pytest.mark.asyncio
async def test_buy_and_sell_transactions(async_session: AsyncSession):
    """BUY + SELL 혼합: 평단가 유지, 수량 감소 검증"""
    # Setup
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Test Portfolio")
    async_session.add(portfolio)
    await async_session.flush()
    
    asset = Asset(symbol="ETH", name="Ethereum", category="Crypto")
    async_session.add(asset)
    await async_session.flush()
    
    # Transaction 1: BUY 10 @ $100
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=10.0,
        price=100.0,
        executed_at=datetime(2026, 1, 1, 10, 0, 0)
    )
    async_session.add(tx1)
    
    # Transaction 2: BUY 5 @ $120
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=5.0,
        price=120.0,
        executed_at=datetime(2026, 1, 2, 10, 0, 0)
    )
    async_session.add(tx2)
    
    # Transaction 3: SELL 7 @ $110
    tx3 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="SELL",
        quantity=7.0,
        price=110.0,
        executed_at=datetime(2026, 1, 3, 10, 0, 0)
    )
    async_session.add(tx3)
    await async_session.commit()
    
    # Execute
    positions = await calculate_positions_from_transactions(async_session, portfolio.id)
    
    # Assert
    assert len(positions) == 1
    pos = positions[0]
    assert pos.quantity == 8.0  # 15 - 7
    # 평단가는 유지: (10*100 + 5*120) / 15 = 106.67
    assert abs(pos.avg_price - 106.67) < 0.01


@pytest.mark.asyncio
async def test_multiple_assets(async_session: AsyncSession):
    """여러 Asset의 Transaction: Asset별 독립 계산 검증"""
    # Setup
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Test Portfolio")
    async_session.add(portfolio)
    await async_session.flush()
    
    asset1 = Asset(symbol="BTC", name="Bitcoin", category="Crypto")
    asset2 = Asset(symbol="ETH", name="Ethereum", category="Crypto")
    async_session.add_all([asset1, asset2])
    await async_session.flush()
    
    # BTC Transactions
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset1.id,
        type="BUY",
        quantity=1.0,
        price=50000.0,
        executed_at=datetime(2026, 1, 1, 10, 0, 0)
    )
    async_session.add(tx1)
    
    # ETH Transactions
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset2.id,
        type="BUY",
        quantity=10.0,
        price=3000.0,
        executed_at=datetime(2026, 1, 2, 10, 0, 0)
    )
    async_session.add(tx2)
    await async_session.commit()
    
    # Execute
    positions = await calculate_positions_from_transactions(async_session, portfolio.id)
    
    # Assert
    assert len(positions) == 2
    
    btc_pos = next((p for p in positions if p.asset_symbol == "BTC"), None)
    eth_pos = next((p for p in positions if p.asset_symbol == "ETH"), None)
    
    assert btc_pos is not None
    assert btc_pos.quantity == 1.0
    assert btc_pos.avg_price == 50000.0
    
    assert eth_pos is not None
    assert eth_pos.quantity == 10.0
    assert eth_pos.avg_price == 3000.0


@pytest.mark.asyncio
async def test_sell_all_returns_no_position(async_session: AsyncSession):
    """모든 수량을 SELL하면 Position이 반환되지 않음"""
    # Setup
    user = User(email="test@example.com", hashed_password="hashed")
    async_session.add(user)
    await async_session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Test Portfolio")
    async_session.add(portfolio)
    await async_session.flush()
    
    asset = Asset(symbol="BTC", name="Bitcoin", category="Crypto")
    async_session.add(asset)
    await async_session.flush()
    
    # BUY 10
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=10.0,
        price=100.0,
        executed_at=datetime(2026, 1, 1, 10, 0, 0)
    )
    async_session.add(tx1)
    
    # SELL 10
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="SELL",
        quantity=10.0,
        price=110.0,
        executed_at=datetime(2026, 1, 2, 10, 0, 0)
    )
    async_session.add(tx2)
    await async_session.commit()
    
    # Execute
    positions = await calculate_positions_from_transactions(async_session, portfolio.id)
    
    # Assert
    assert len(positions) == 0
