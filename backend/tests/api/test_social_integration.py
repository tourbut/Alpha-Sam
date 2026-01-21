import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.main import app
from app.src.core.db import get_session
from app.src.deps import get_current_user

from app.src.models.user import User
from app.src.models.social import UserFollow, LeaderboardRank, LeaderboardPeriod

@pytest_asyncio.fixture
async def setup_users(test_session: AsyncSession):
    # Create 2 Users
    user1 = User(email="user1@example.com", username="user1", nickname="Nick1", hashed_password="pw", is_active=True)
    user2 = User(email="user2@example.com", username="user2", nickname="Nick2", hashed_password="pw", is_active=True)
    test_session.add(user1)
    test_session.add(user2)
    await test_session.commit()
    await test_session.refresh(user1)
    await test_session.refresh(user2)
    return user1, user2

@pytest.mark.asyncio
async def test_follow_unfollow_flow(test_session: AsyncSession, setup_users):
    user1, user2 = setup_users
    
    # Override CurrentUser to be user1
    async def get_current_user_override():
        return user1

    async def get_session_override():
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Follow User2
        response = await ac.post(f"/api/v1/social/follow/{user2.id}")
        assert response.status_code == 201
        data = response.json()
        assert data["following_id"] == user2.id
        assert data["follower_id"] == user1.id

        # 2. Check Followers of User2
        response = await ac.get(f"/api/v1/social/users/{user2.id}/followers")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["users"][0]["id"] == user1.id

        # 3. Check Following of User1
        response = await ac.get(f"/api/v1/social/users/{user1.id}/following")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["users"][0]["id"] == user2.id

        # 4. Unfollow User2
        response = await ac.delete(f"/api/v1/social/follow/{user2.id}")
        assert response.status_code == 204

        # 5. Verify Unfollowed
        response = await ac.get(f"/api/v1/social/users/{user2.id}/followers")
        assert response.json()["total"] == 0

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_leaderboard_simple(test_session: AsyncSession, setup_users):
    user1, user2 = setup_users
    
    # Need at least one portfolio for the mandatory portfolio_id in LeaderboardRank
    from app.src.models.portfolio import Portfolio
    p1 = Portfolio(name="P1", owner_id=user1.id, total_value=10000.0)
    p2 = Portfolio(name="P2", owner_id=user2.id, total_value=5000.0)
    test_session.add(p1)
    test_session.add(p2)
    await test_session.commit()
    await test_session.refresh(p1)
    await test_session.refresh(p2)

    # Manually insert some rankings for testing
    rank1 = LeaderboardRank(user_id=user1.id, portfolio_id=p1.id, period=LeaderboardPeriod.ALL_TIME, return_rate=15.5, total_value=10000.0, rank=1)
    rank2 = LeaderboardRank(user_id=user2.id, portfolio_id=p2.id, period=LeaderboardPeriod.ALL_TIME, return_rate=5.2, total_value=5000.0, rank=2)
    test_session.add(rank1)
    test_session.add(rank2)
    await test_session.commit()

    # Note: leaderboard_service would normally fetch from Redis first.
    # We should mock get_top_n or ensure service is test-ready.
    # In routes/social.py, it calls leaderboard_service.get_top_n.
    
    from unittest.mock import patch
    with patch("app.src.services.leaderboard_service.leaderboard_service.get_top_n") as mock_get:
        mock_get.return_value = [(user1.id, 15.5), (user2.id, 5.2)]
        
        async def get_session_override():
            yield test_session

        app.dependency_overrides[get_session] = get_session_override

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/v1/social/leaderboard")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["nickname"] == user1.nickname
            assert data[0]["return_rate"] == 15.5
            assert data[0]["total_value"] == 10000.0

    app.dependency_overrides = {}
