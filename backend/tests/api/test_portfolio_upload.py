import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import tempfile
import pdfplumber
from unittest.mock import patch, AsyncMock

from app.main import app
from app.src.core.db import get_session
from app.src.deps import get_current_user
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction
from app.src.models.user import User

@pytest.fixture
def mock_parsed_transactions():
    from app.src.schemas.transaction_common import CommonTransaction
    from datetime import datetime
    return [
        CommonTransaction(
            date=datetime(2026, 1, 13),
            type="BUY",
            name="골드만삭스 나스닥 100 코어 프리미엄 인컴 ETF",
            ticker="GPIQ",
            quantity=10.0,
            price=50.0,
            currency="USD",
            fee=0.0
        ),
        CommonTransaction(
            date=datetime(2026, 1, 14),
            type="SELL",
            name="브로드컴",
            ticker="AVGO",
            quantity=2.0,
            price=1500.0,
            currency="USD",
            fee=0.0
        )
    ]

@pytest.mark.asyncio
async def test_upload_toss_portfolio_success(
    test_session: AsyncSession
):
    # Setup test user
    user = User(email="test@example.com", username="test", nickname="TestUser", hashed_password="pw", is_active=True)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    async def get_current_user_override():
        return user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    # Mock the CommonTransaction so we don't need a real PDF
    with patch('app.src.services.parsers.toss.TossParser.parse', new_callable=AsyncMock) as mock_parse_pdf:
        # Import the fixture data directly inside the test to avoid passing it
        from app.src.schemas.transaction_common import CommonTransaction
        from datetime import datetime
        mock_parse_pdf.return_value = [
            CommonTransaction(
                date=datetime(2026, 1, 13),
                type="BUY",
                name="골드만삭스 나스닥 100 코어 프리미엄 인컴 ETF",
                ticker="GPIQ",
                quantity=10.0,
                price=50.0,
                currency="USD",
                fee=0.0
            ),
            CommonTransaction(
                date=datetime(2026, 1, 14),
                type="SELL",
                name="브로드컴",
                ticker="AVGO",
                quantity=2.0,
                price=1500.0,
                currency="USD",
                fee=0.0
            )
        ]
        
        file_content = b"dummy pdf content"
        files = {"file": ("test_toss.pdf", file_content, "application/pdf")}
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/portfolios/upload/toss",
                files=files
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["message"] == "Successfully added 2 transactions to portfolio."
            assert data["transaction_count"] == 2
            assert "portfolio_id" in data
            
            portfolio_id = uuid.UUID(data["portfolio_id"])
            
            # Verify DB records
            from sqlalchemy import select
            
            # 1. Check Portfolio
            result = await test_session.execute(select(Portfolio).where(Portfolio.id == portfolio_id))
            portfolio = result.scalars().first()
            assert portfolio is not None
            assert portfolio.name == "토스증권 포트폴리오(자동생성)"
            assert portfolio.owner_id == user.id
            
            # 2. Check Assets
            result = await test_session.execute(select(Asset).where(Asset.portfolio_id == portfolio_id))
            assets = result.scalars().all()
            assert len(assets) == 2
            asset_symbols = [a.symbol for a in assets]
            assert "GPIQ" in asset_symbols
            assert "AVGO" in asset_symbols
            
            # 3. Check Transactions
            result = await test_session.execute(select(Transaction).where(Transaction.portfolio_id == portfolio_id))
            transactions = result.scalars().all()
            assert len(transactions) == 2

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_upload_toss_portfolio_invalid_file_extension(
    test_session: AsyncSession
):
    # Setup test user
    user = User(email="test2@example.com", username="test2", nickname="TestUser2", hashed_password="pw", is_active=True)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    async def get_current_user_override():
        return user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    file_content = b"dummy content"
    files = {"file": ("test_toss.txt", file_content, "text/plain")}
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/portfolios/upload/toss",
            files=files
        )
        
        assert response.status_code == 400
        assert "Only PDF files are supported" in response.json()["detail"]

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_upload_toss_portfolio_empty_parsing_result(
    test_session: AsyncSession
):
    # Setup test user
    user = User(email="test3@example.com", username="test3", nickname="TestUser3", hashed_password="pw", is_active=True)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    async def get_current_user_override():
        return user

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    # Mock parse to return empty list
    with patch('app.src.services.parsers.toss.TossParser.parse', new_callable=AsyncMock) as mock_parse_pdf:
        mock_parse_pdf.return_value = []
        
        file_content = b"dummy pdf content without transactions"
        files = {"file": ("test_empty.pdf", file_content, "application/pdf")}
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/portfolios/upload/toss",
                files=files
            )
            
            assert response.status_code == 400
            assert "No transactions found" in response.json()["detail"]

    app.dependency_overrides = {}
