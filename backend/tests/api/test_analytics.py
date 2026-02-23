import pytest
from httpx import AsyncClient
import uuid
from datetime import datetime, date, timedelta

from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction

@pytest.fixture
async def analytics_test_data(db_session, test_user):
    """
    Setup dummy data for analytics tests:
    - 1 Portfolio
    - 2 Assets (AAPL, CASH)
    - 3 Transactions
    """
    # 1. 포트폴리오 생성
    portfolio = Portfolio(
        owner_id=test_user.id,
        name="Analytics Test Portfolio",
        currency="USD"
    )
    db_session.add(portfolio)
    await db_session.flush()

    # 2. 자산 생성
    asset_aapl = Asset(
        symbol="AAPL",
        name="Apple Inc.",
        category="STOCK"
    )
    asset_cash = Asset(
        symbol="CASH",
        name="US Dollar",
        category="CASH"
    )
    db_session.add(asset_aapl)
    db_session.add(asset_cash)
    await db_session.flush()

    # 3. 거래 내역 생성
    today = date.today()
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_cash.id,
        type="BUY",
        quantity=10000.0,
        price=1.0,  # 1달러 = 1단위 (Cash)
        executed_at=datetime.combine(today - timedelta(days=10), datetime.min.time())
    )
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_aapl.id,
        type="BUY",
        quantity=10.0,
        price=150.0,
        executed_at=datetime.combine(today - timedelta(days=5), datetime.min.time())
    )
    tx3 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_cash.id,
        type="SELL",
        quantity=1500.0, # AAPL 매수에 사용된 현금
        price=1.0,
        executed_at=datetime.combine(today - timedelta(days=5), datetime.min.time())
    )
    
    db_session.add(tx1)
    db_session.add(tx2)
    db_session.add(tx3)
    await db_session.commit()

    return {
        "portfolio": portfolio,
        "assets": {"AAPL": asset_aapl, "CASH": asset_cash},
        "transactions": [tx1, tx2, tx3]
    }

@pytest.mark.asyncio
async def test_get_portfolio_allocation(async_client: AsyncClient, user_token_headers: dict, analytics_test_data: dict):
    portfolio_id = analytics_test_data["portfolio"].id
    
    response = await async_client.get(
        f"/api/v1/analytics/portfolio/{portfolio_id}/allocation",
        headers=user_token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2 # AAPL, CASH
    
    # Sort or find
    aapl_data = next((item for item in data if item["ticker"] == "AAPL"), None)
    cash_data = next((item for item in data if item["ticker"] == "CASH"), None)
    
    assert aapl_data is not None
    assert cash_data is not None
    
    # AAPL: 10 * 150 = 1500 value
    assert aapl_data["total_value"] == 1500.0
    
    # CASH: 10000 - 1500 = 8500 value
    assert cash_data["total_value"] == 8500.0
    
    # Total = 10000. AAPL% = 15.0%, CASH% = 85.0%
    assert aapl_data["percentage"] == 15.0
    assert cash_data["percentage"] == 85.0

@pytest.mark.asyncio
async def test_get_portfolio_history(async_client: AsyncClient, user_token_headers: dict, analytics_test_data: dict):
    portfolio_id = analytics_test_data["portfolio"].id
    
    response = await async_client.get(
        f"/api/v1/analytics/portfolio/{portfolio_id}/history?range=1M",
        headers=user_token_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Needs at least one day
    assert len(data) > 0
    
    # latest value should reflect cumulative invested (rough mock logic in service)
    # Total invested over time: initially 10k cash -> then swap 1.5k cash for AAPL
    # But current logic is naive mock, so just verifying structure and runability.
    latest = data[-1]
    assert "date" in latest
    assert "total_value" in latest
    assert "uninvested_cash" in latest
