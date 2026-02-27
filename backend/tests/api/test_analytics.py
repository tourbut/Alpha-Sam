import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import uuid
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.src.core.db import get_session
from app.src.deps import get_current_user
from app.src.models.user import User
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction

@pytest_asyncio.fixture
async def analytics_test_data(test_session: AsyncSession):
    """
    Setup dummy data for analytics tests:
    - 1 User
    - 1 Portfolio
    - 2 Assets (AAPL, CASH)
    - 3 Transactions
    """
    # 0. User creation
    test_user = User(email="analytics@example.com", username="analytics_user", nickname="Ana", hashed_password="pw", is_active=True)
    test_session.add(test_user)
    await test_session.commit()
    await test_session.refresh(test_user)

    # 1. Portfolio creation
    portfolio = Portfolio(
        owner_id=test_user.id,
        name="Analytics Test Portfolio",
        currency="USD"
    )
    test_session.add(portfolio)
    await test_session.flush()

    # 2. Asset creation
    asset_aapl = Asset(
        symbol="AAPL",
        name="Apple Inc.",
        category="STOCK",
        portfolio_id=portfolio.id,
        owner_id=test_user.id
    )
    asset_cash = Asset(
        symbol="CASH",
        name="US Dollar",
        category="CASH",
        portfolio_id=portfolio.id,
        owner_id=test_user.id
    )
    test_session.add(asset_aapl)
    test_session.add(asset_cash)
    await test_session.flush()

    # 3. Transaction creation
    today = date.today()
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset_cash.id,
        type="BUY",
        quantity=10000.0,
        price=1.0,
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
        quantity=1500.0, 
        price=1.0,
        executed_at=datetime.combine(today - timedelta(days=5), datetime.min.time())
    )
    
    test_session.add(tx1)
    test_session.add(tx2)
    test_session.add(tx3)
    await test_session.commit()

    return {
        "user": test_user,
        "portfolio": portfolio,
        "assets": {"AAPL": asset_aapl, "CASH": asset_cash},
        "transactions": [tx1, tx2, tx3]
    }

@pytest.mark.asyncio
async def test_get_portfolio_allocation(test_session: AsyncSession, analytics_test_data: dict):
    test_user = analytics_test_data["user"]
    portfolio_id = analytics_test_data["portfolio"].id
    
    async def get_current_user_override():
        return test_user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/analytics/portfolio/{portfolio_id}/allocation")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2 
        
        aapl_data = next((item for item in data if item["ticker"] == "AAPL"), None)
        cash_data = next((item for item in data if item["ticker"] == "CASH"), None)
        
        assert aapl_data is not None
        assert cash_data is not None
        assert aapl_data["total_value"] == 1500.0
        assert cash_data["total_value"] == 8500.0
        assert aapl_data["percentage"] == 15.0
        assert cash_data["percentage"] == 85.0

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_get_portfolio_history(test_session: AsyncSession, analytics_test_data: dict):
    test_user = analytics_test_data["user"]
    portfolio_id = analytics_test_data["portfolio"].id
    
    async def get_current_user_override():
        return test_user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/analytics/portfolio/{portfolio_id}/history?range=1M")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        latest = data[-1]
        assert "date" in latest
        assert "total_value" in latest
        assert "uninvested_cash" in latest

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_get_portfolios_allocation_aggregated(test_session: AsyncSession, analytics_test_data: dict):
    test_user = analytics_test_data["user"]
    user_id = test_user.id
    
    portfolio2 = Portfolio(
        owner_id=user_id,
        name="Portfolio 2",
        currency="USD"
    )
    test_session.add(portfolio2)
    await test_session.flush()

    today = date.today()
    tx_p2 = Transaction(
        portfolio_id=portfolio2.id,
        asset_id=analytics_test_data["assets"]["AAPL"].id,
        type="BUY",
        quantity=5.0,
        price=150.0,
        executed_at=datetime.combine(today - timedelta(days=2), datetime.min.time())
    )
    test_session.add(tx_p2)
    await test_session.commit()

    async def get_current_user_override():
        return test_user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/analytics/portfolios/allocation")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2 
        
        aapl_data = next((item for item in data if item["ticker"] == "AAPL"), None)
        assert aapl_data is not None
        assert aapl_data["total_value"] == 2250.0

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_get_portfolios_history_aggregated(test_session: AsyncSession, analytics_test_data: dict):
    test_user = analytics_test_data["user"]
    
    async def get_current_user_override():
        return test_user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/analytics/portfolios/history?range=1M")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        latest = data[-1]
        assert "date" in latest
        assert "total_value" in latest
        assert "uninvested_cash" in latest

    app.dependency_overrides = {}
