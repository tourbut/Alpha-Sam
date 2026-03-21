import pytest
import uuid
import random
import string
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.src.models.user import User
from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.services.portfolio_service import PortfolioService
from app.src.core.db import settings

# Create a clean engine for tests to avoid loop conflicts
@pytest.fixture
async def test_session():
    # Use database_url from settings
    engine = create_async_engine(settings.database_url, echo=False, future=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await engine.dispose()

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@pytest.mark.asyncio
async def test_update_portfolio_visibility(test_session: AsyncSession):
    """
    Portfolio Visibility 업데이트 및 share_token 생성/제거 테스트
    """
    session = test_session
    rand_suffix = random_string()
    
    # 1. Setup
    user = User(email=f"test_social_{rand_suffix}@example.com", hashed_password="hashed")
    session.add(user)
    await session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Social Portfolio")
    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)
    
    assert portfolio.visibility == PortfolioVisibility.PRIVATE
    assert portfolio.share_token is None
    
    # 2. Update to PUBLIC
    updated = await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.PUBLIC)
    assert updated.visibility == PortfolioVisibility.PUBLIC
    
    # 3. Update to LINK_ONLY
    updated = await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.LINK_ONLY)
    assert updated.visibility == PortfolioVisibility.LINK_ONLY
    assert updated.share_token is not None
    token = updated.share_token
    
    # 4. Update to PRIVATE
    updated = await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.PRIVATE)
    assert updated.visibility == PortfolioVisibility.PRIVATE
    assert updated.share_token is None
    
    # 5. Update back to LINK_ONLY (New token)
    updated = await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.LINK_ONLY)
    assert updated.share_token is not None
    assert updated.share_token != token

@pytest.mark.asyncio
async def test_get_shared_portfolio(test_session: AsyncSession):
    """
    공유된 포트폴리오 조회 (get_shared_portfolio) 테스트
    """
    session = test_session
    rand_suffix = random_string()
    
    # 1. Setup
    user = User(email=f"share_test_{rand_suffix}@example.com", hashed_password="hashed", nickname="Sharer")
    session.add(user)
    await session.flush()
    
    portfolio = Portfolio(owner_id=user.id, name="Shared Portfolio")
    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)
    
    # Initial PRIVATE -> None
    # LINK_ONLY가 아닌 PRIVATE 상태의 포트폴리오에 대해 임의의 토큰으로 조회 시도
    result = await PortfolioService.get_shared_portfolio(session, uuid.uuid4())
    assert result is None
    
    # 2. Set to LINK_ONLY
    updated = await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.LINK_ONLY)
    token = updated.share_token
    
    # 3. Success with token
    shared_pf = await PortfolioService.get_shared_portfolio(session, token)
    assert shared_pf is not None
    assert shared_pf.id == portfolio.id
    assert shared_pf.visibility == PortfolioVisibility.LINK_ONLY
    
    # 4. Fail with wrong token
    result = await PortfolioService.get_shared_portfolio(session, uuid.uuid4())
    assert result is None
    
    # 5. Fail after revert to PRIVATE
    await PortfolioService.update_visibility(session, portfolio.id, PortfolioVisibility.PRIVATE)
    result = await PortfolioService.get_shared_portfolio(session, token)
    assert result is None
