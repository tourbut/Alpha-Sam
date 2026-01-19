import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.models.position import Position
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.user import User

# NOTE: This test assumes DB setup and auth fixtures are available.
# Since I cannot see conftest.py, I will write a standalone-style test logic 
# that can be integrated or acts as a guide.

@pytest.mark.asyncio
async def test_create_transaction_updates_position(
    async_client: AsyncClient,
    test_session: AsyncSession,
    test_user_token: str, # Mock fixture
    test_portfolio: Portfolio, # Mock fixture
    test_asset: Asset # Mock fixture
):
    """
    Test that creating a BUY transaction correctly creates/updates a Position via Hybrid Approach.
    """
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # 1. Create BUY Transaction
    payload = {
        "portfolio_id": test_portfolio.id,
        "asset_id": test_asset.id,
        "type": "BUY",
        "quantity": 10.0,
        "price": 100.0, # Total Value 1000
        "executed_at": "2026-01-01T00:00:00Z"
    }
    
    response = await async_client.post("/api/v1/transactions", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 10.0
    
    # 2. Verify Position Created
    stmt = select(Position).where(
        Position.portfolio_id == test_portfolio.id,
        Position.asset_id == test_asset.id
    )
    result = await test_session.execute(stmt)
    position = result.scalar_one_or_none()
    
    assert position is not None
    assert position.quantity == 10.0
    assert position.avg_price == 100.0
    
    # 3. Create Another BUY Update (Average Price Check)
    payload2 = {
        "portfolio_id": test_portfolio.id,
        "asset_id": test_asset.id,
        "type": "BUY",
        "quantity": 10.0,
        "price": 200.0, # Total Value 2000
    }
    # New Avg = (1000 + 2000) / 20 = 150
    
    response = await async_client.post("/api/v1/transactions", json=payload2, headers=headers)
    assert response.status_code == 200

    # Refresh Position
    await test_session.refresh(position)
    assert position.quantity == 20.0
    assert position.avg_price == 150.0

