import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.src.core.db import AsyncSessionLocal
from app.src.models.user import User
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from sqlalchemy import select

@pytest.mark.asyncio(loop_scope="session")
async def test_cash_asset_transaction_creation():
    uid = uuid.uuid4()
    
    # 0. Create Test User
    async with AsyncSessionLocal() as session:
        user = User(id=uid, email=f"test{uid}@example.com", hashed_password="path", is_active=True)
        session.add(user)
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create Portfolio
        portfolio_res = await client.post(
            "/api/v1/portfolios",
            json={"name": "Test Cash Portfolio", "currency": "USD", "description": "test"},
            headers={"X-User-Id": str(uid)}
        )
        assert portfolio_res.status_code in [200, 201]
        portfolio_id = portfolio_res.json()["id"]

        # 2. Create Cash Asset
        asset_res = await client.post(
            "/api/v1/assets",
            json={
                "portfolio_id": portfolio_id,
                "symbol": "CASH-USD",
                "name": "US Dollar",
                "category": "cash"
            },
            headers={"X-User-Id": str(uid)}
        )
        assert asset_res.status_code in [200, 201]
        asset_id = asset_res.json()["id"]

        # 3. Create Cash Transaction (amount only)
        tx_res = await client.post(
            f"/api/v1/portfolios/{portfolio_id}/transactions",
            json={
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "type": "BUY",
                "amount": 5000.0
            },
            headers={"X-User-Id": str(uid)}
        )
        assert tx_res.status_code in [200, 201]
        tx_data = tx_res.json()
        assert tx_data["price"] == 1.0
        assert tx_data["quantity"] == 5000.0

        # 4. Create Normal Asset (Error Case)
        asset_res2 = await client.post(
            "/api/v1/assets",
            json={
                "portfolio_id": portfolio_id,
                "symbol": "AAPL",
                "name": "Apple",
                "category": "stock"
            },
            headers={"X-User-Id": str(uid)}
        )
        asset_id2 = asset_res2.json()["id"]

        tx_res2 = await client.post(
            f"/api/v1/portfolios/{portfolio_id}/transactions",
            json={
                "portfolio_id": portfolio_id,
                "asset_id": asset_id2,
                "type": "BUY",
                "amount": 5000.0
            },
            headers={"X-User-Id": str(uid)}
        )
        # Expect 400 or 422
        assert tx_res2.status_code in [400, 422]

