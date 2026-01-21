import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.src.core.db import get_session
from app.src.deps import get_current_user
from app.src.models.user import User
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction
from app.src.models.price import Price
import pytest_asyncio

@pytest_asyncio.fixture
async def setup_user(test_session: AsyncSession):
    # 1. Create User
    rand_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"asset_test_{rand_id}@example.com", 
        username=f"asset_test_{rand_id}", 
        nickname=f"AssetTester_{rand_id}", 
        hashed_password="pw", 
        is_active=True
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_read_portfolio_asset_summary(test_session: AsyncSession, setup_user):
    user = setup_user
    
    # 1. Setup Portfolio
    portfolio = Portfolio(
        owner_id=user.id,
        name="Asset Detail Test Portfolio",
        description="Testing asset details"
    )
    test_session.add(portfolio)
    await test_session.commit()
    await test_session.refresh(portfolio)

    # 2. Setup Asset (Linked to Portfolio)
    asset = Asset(
        portfolio_id=portfolio.id,
        symbol="BTC", 
        name="Bitcoin", 
        category="CRYPTO"
    )
    test_session.add(asset)
    await test_session.commit()
    await test_session.refresh(asset)

    # 3. Add Transactions (Buy BTC)
    # Transaction 1: Buy 1.0 at 50000
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=1.0,
        price=50000.0,
        executed_at=datetime.utcnow()
    )
    test_session.add(tx1)
    
    # Transaction 2: Buy 0.5 at 40000
    tx2 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=0.5,
        price=40000.0,
        executed_at=datetime.utcnow()
    )
    test_session.add(tx2)
    
    # Add Price (Current Price)
    price = Price(
        asset_id=asset.id,
        value=60000.0,
        timestamp=datetime.utcnow()
    )
    test_session.add(price)
    
    await test_session.commit()

    # 4. Override Dependencies
    async def get_current_user_override():
        return user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    # 5. Test API Call
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/portfolios/{portfolio.id}/assets/{asset.id}")

        assert response.status_code == 200
        data = response.json()
        
        # 6. Verify Calculations
        # Total Qty: 1.5
        # Total Cost: (1 * 50000) + (0.5 * 40000) = 70000
        # Avg Price: 70000 / 1.5 = 46666.666...
        # Current Price: 60000
        # Total Value: 1.5 * 60000 = 90000
        # Profit Loss: 90000 - 70000 = 20000
        # Return Rate: (20000 / 70000) * 100 = 28.57%
        
        assert data["quantity"] == 1.5
        assert data["total_value"] == 90000.0
        assert data["profit_loss"] == 20000.0
        assert abs(data["avg_price"] - 46666.67) < 0.1
        assert abs(data["return_rate"] - 28.57) < 0.1
        assert data["current_price"] == 60000.0

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_read_asset_transactions(test_session: AsyncSession, setup_user):
    user = setup_user
    
    # 1. Setup Portfolio
    portfolio = Portfolio(
        owner_id=user.id,
        name="Tx Test Portfolio",
        description="Testing transactions list"
    )
    test_session.add(portfolio)
    await test_session.commit()
    await test_session.refresh(portfolio)

    # 2. Setup Asset
    asset = Asset(
        portfolio_id=portfolio.id,
        symbol="BTC", 
        name="Bitcoin", 
        category="CRYPTO"
    )
    test_session.add(asset)
    await test_session.commit()
    await test_session.refresh(asset)

    # 3. Add Transactions
    tx1 = Transaction(
        portfolio_id=portfolio.id,
        asset_id=asset.id,
        type="BUY",
        quantity=1.0,
        price=50000.0,
        executed_at=datetime.utcnow()
    )
    test_session.add(tx1)
    await test_session.commit()

    # 4. Override Dependencies
    async def get_current_user_override():
        return user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    # 5. Test API Call
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/portfolios/{portfolio.id}/assets/{asset.id}/transactions")

        assert response.status_code == 200
        data = response.json()
        
        # 6. Verify List
        assert len(data) == 1
        assert data[0]["type"] == "buy"
        assert data[0]["quantity"] == 1.0
        assert data[0]["price"] == 50000.0
        assert data[0]["total"] == 50000.0
    
    app.dependency_overrides = {}
