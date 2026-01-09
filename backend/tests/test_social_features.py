import asyncio
import uuid
from app.src.services.leaderboard_service import LeaderboardService
from app.src.schemas.social import PortfolioShareCreate

async def test_leaderboard():
    lb = LeaderboardService(key="test:leaderboard")
    print("Updating scores...")
    await lb.update_score(1, 15.5)
    await lb.update_score(2, 25.0)
    await lb.update_score(3, 10.2)
    
    top_n = await lb.get_top_n(5)
    print(f"Top N: {top_n}")
    assert top_n[0][0] == 2
    assert top_n[0][1] == 25.0
    
    rank = await lb.get_user_rank(1)
    print(f"User 1 rank: {rank}")
    assert rank == 2
    print("Leaderboard test passed!")

if __name__ == "__main__":
    asyncio.run(test_leaderboard())
