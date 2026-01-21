import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.main import app
from app.src.core.db import get_session
from app.src.deps import get_current_user

from app.src.models.position import Position
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.user import User

# Fixtures for this test module specifically
@pytest_asyncio.fixture
async def setup_data(test_session: AsyncSession):
    # Create User
    user = User(email="test@example.com", username="testuser", hashed_password="pw", is_active=True)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    # Create Portfolio
    portfolio = Portfolio(name="Main Portfolio", total_value=0.0, owner_id=user.id)
    test_session.add(portfolio)
    await test_session.commit()
    await test_session.refresh(portfolio)

    # Create Asset
    asset = Asset(symbol="AAPL", name="Apple Inc.", current_price=150.0)
    test_session.add(asset)
    await test_session.commit()
    await test_session.refresh(asset)

    return user, portfolio, asset

@pytest_asyncio.fixture
async def override_deps(test_session, setup_data):
    user, _, _ = setup_data
    
    # Override Session
    async def get_session_override():
        yield test_session

    # Override User
    async def get_current_user_override():
        return user

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    yield
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_create_transaction_updates_position(
    test_session: AsyncSession,
    setup_data,
    override_deps
):
    """
    Test that creating a BUY transaction correctly creates/updates a Position via Hybrid Approach.
    """
    user, portfolio, asset = setup_data
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Create BUY Transaction
        payload = {
            "portfolio_id": portfolio.id,
            "asset_id": asset.id,
            "type": "BUY",
            "quantity": 10.0,
            "price": 100.0, # Total Value 1000, Avg Price 100
            "executed_at": "2026-01-01T00:00:00Z"
        }
        
        response = await ac.post("/api/v1/transactions", json=payload)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["quantity"] == 10.0
        
        # 2. Verify Position Created
        # Run query directly on Session
        stmt = select(Position).where(
            Position.portfolio_id == portfolio.id,
            Position.asset_id == asset.id
        )
        result = await test_session.execute(stmt)
        position = result.scalar_one_or_none()
        
        assert position is not None
        assert float(position.quantity) == 10.0
        assert float(position.avg_price) == 100.0
        
        # 3. Create Another BUY Update (Average Price Check)
        payload2 = {
            "portfolio_id": portfolio.id,
            "asset_id": asset.id,
            "type": "BUY",
            "quantity": 10.0,
            "price": 200.0, # Total Value 2000
             "executed_at": "2026-01-02T00:00:00Z"
        }
        # New Avg = (1000 + 2000) / 20 = 150
        
        response = await ac.post("/api/v1/transactions", json=payload2)
        assert response.status_code == 200

        # Re-query Position to get latest data
        result = await test_session.execute(stmt)
        position = result.scalar_one_or_none()
        
        assert float(position.quantity) == 20.0
        assert float(position.avg_price) == 150.0

@pytest.mark.asyncio
async def test_create_transaction_sell_logic(
    test_session: AsyncSession,
    setup_data,
    override_deps
):
    """
    Test that creating a SELL transaction correctly updates Position.
    """
    user, portfolio, asset = setup_data
    
    # Pre-condition: Have 20 quantity (from previous logic, but setup_data is clean in fixture? 
    # Default fixture scope is function? verifying...)
    # Yes, pytest fixtures are function scope by default. So clean state.
    
    # Setup: Buy 20 @ 100
    pos = Position(portfolio_id=portfolio.id, asset_id=asset.id, quantity=20.0, avg_price=100.0)
    test_session.add(pos)
    await test_session.commit()
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. SELL 5
        payload = {
            "portfolio_id": portfolio.id,
            "asset_id": asset.id,
            "type": "SELL",
            "quantity": 5.0,
            "price": 120.0, 
            "executed_at": "2026-01-03T00:00:00Z"
        }
        
        response = await ac.post("/api/v1/transactions", json=payload)
        assert response.status_code == 200
        
        # Verify Position
        await test_session.refresh(pos)
        assert float(pos.quantity) == 15.0
        assert float(pos.avg_price) == 100.0 # Avg price doesn't change on SELL

        # 2. Assert Insufficient Quantity
        payload_fail = {
            "portfolio_id": portfolio.id,
            "asset_id": asset.id,
            "type": "SELL",
            "quantity": 20.0, # have 15
            "price": 120.0, 
            "executed_at": "2026-01-04T00:00:00Z"
        }
        response = await ac.post("/api/v1/transactions", json=payload_fail)
        assert response.status_code == 400
        assert "Insufficient quantity" in response.text
