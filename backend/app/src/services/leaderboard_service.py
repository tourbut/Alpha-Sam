from typing import List, Tuple, Optional
from app.src.core.cache import get_redis_client

class LeaderboardService:
    """
    Redis를 이용한 리더보드 관리 서비스
    """
    def __init__(self, key: str = "leaderboard:weekly"):
        self.key = key

    async def update_score(self, user_id: int, pnl_percent: float):
        """
        사용자의 수익률 점수 업데이트 (ZADD)
        """
        client = await get_redis_client()
        await client.zadd(self.key, {str(user_id): pnl_percent})

    async def get_top_n(self, n: int = 10) -> List[Tuple[int, float]]:
        """
        상위 N명의 리더보드 조회 (ZRANGE)
        """
        client = await get_redis_client()
        # ZRANGE key +inf -inf BYSCORE REV LIMIT 0 N
        # 또는 단순 ZREVRANGE 사용
        results = await client.zrevrange(self.key, 0, n - 1, withscores=True)
        return [(int(user_id), float(score)) for user_id, score in results]

    async def get_user_rank(self, user_id: int) -> Optional[int]:
        """
        특정 사용자의 순위 조회 (ZREVRANK)
        """
        client = await get_redis_client()
        rank = await client.zrevrank(self.key, str(user_id))
        return rank + 1 if rank is not None else None

leaderboard_service = LeaderboardService()
