import pytest
from datetime import datetime
from sqlalchemy import select
from app.src.models.user import User
from app.src.models.portfolio import Portfolio
from app.src.models.social import UserFollow, LeaderboardPeriod, LeaderboardRank
from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.models.transaction import Transaction
from app.src.services.leaderboard_service import leaderboard_service

@pytest.mark.asyncio
async def test_follow_unfollow(test_session, random_email, random_nickname):
    # Setup users
    user1 = User(email=random_email, hashed_password="pw", nickname=random_nickname)
    user2 = User(email="f"+random_email, hashed_password="pw", nickname="f"+random_nickname)
    test_session.add_all([user1, user2])
    await test_session.commit()
    await test_session.refresh(user1)
    await test_session.refresh(user2)
    
    # Follow
    follow = UserFollow(follower_id=user1.id, following_id=user2.id)
    test_session.add(follow)
    await test_session.commit()
    
    # Check Following List
    stmt = select(UserFollow).where(UserFollow.follower_id == user1.id)
    res = await test_session.execute(stmt)
    following_list = res.scalars().all()
    assert len(following_list) == 1
    assert following_list[0].following_id == user2.id
    
    # Check Followers List
    stmt = select(UserFollow).where(UserFollow.following_id == user2.id)
    res = await test_session.execute(stmt)
    follower_list = res.scalars().all()
    assert len(follower_list) == 1
    assert follower_list[0].follower_id == user1.id
    
    # Unfollow
    await test_session.delete(follow)
    await test_session.commit()
    
    # Check
    stmt = select(UserFollow).where(UserFollow.follower_id == user1.id)
    res = await test_session.execute(stmt)
    assert len(res.scalars().all()) == 0

@pytest.mark.asyncio
async def test_leaderboard_calculation(test_session, random_email):
    # Setup User & Portfolio
    user = User(email=random_email, hashed_password="pw", nickname="RankUser")
    test_session.add(user)
    await test_session.flush()
    
    # is_primary_for_leaderboard=True 필수
    pf = Portfolio(owner_id=user.id, name="RankPF", is_primary_for_leaderboard=True)
    test_session.add(pf)
    await test_session.flush()
    
    # Setup Asset
    asset = Asset(symbol="TEST_RANK", name="Test Rank Coin", category="Crypto")
    test_session.add(asset)
    await test_session.flush()
    
    # Setup Price (Current price = 200)
    price = Price(asset_id=asset.id, value=200.0, timestamp=datetime.utcnow())
    test_session.add(price)
    
    # Setup Transaction (Buy 1 at 100) -> Return 100%
    tx = Transaction(
        portfolio_id=pf.id, asset_id=asset.id, type="BUY", 
        quantity=1.0, price=100.0, executed_at=datetime.utcnow()
    )
    test_session.add(tx)
    await test_session.commit()
    
    # Calculate Leaderboard
    # Redis might fail in test environment, but DB fallback logic should work via exception handling in service
    try:
        count = await leaderboard_service.calculate_leaderboard(test_session, LeaderboardPeriod.ALL_TIME)
        # count depends on pre-existing data too, so at least 1
        assert count >= 1
    except Exception as e:
        pytest.fail(f"Leaderboard calculation failed: {e}")
    
    # Verify via get_top_n (DB fallback)
    # Redis might not be running, so get_top_n logic relies on Service handling exception
    # To force DB fallback, we pass session
    ranks = await leaderboard_service.get_top_n(100, LeaderboardPeriod.ALL_TIME, session=test_session)
    
    found = False
    for uid, rate in ranks:
        if uid == user.id:
            assert rate == 100.0
            found = True
            break
    assert found
