from typing import List, Tuple, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.core.cache import get_redis_client
from app.src.models.social import LeaderboardRank, LeaderboardPeriod
from app.src.models.portfolio import Portfolio
from app.src.services.portfolio_service import PortfolioService
import logging

logger = logging.getLogger(__name__)

class LeaderboardService:
    """
    Redis + DB Hybrid Leaderboard Service
    """
    def __init__(self, key_prefix: str = "leaderboard"):
        self.key_prefix = key_prefix

    def _get_redis_key(self, period: LeaderboardPeriod) -> str:
        return f"{self.key_prefix}:{period.value.lower()}"

    async def calculate_leaderboard(self, session: AsyncSession, period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME) -> int:
        """
        리더보드 계산 및 갱신 (DB + Redis)
        현재는 ALL_TIME 수익률만 계산
        """
        # 1. 대상 포트폴리오 조회: is_primary_for_leaderboard=True
        stmt = select(Portfolio).where(Portfolio.is_primary_for_leaderboard == True)
        result = await session.execute(stmt)
        portfolios = result.scalars().all()

        ranking_data = [] # List[Dict]

        for pf in portfolios:
            try:
                # Use PortfolioService to get positions with calculated metrics (valuation, etc.)
                positions = await PortfolioService.get_positions(session, pf.id)
                
                total_current_value = 0.0
                total_invested = 0.0
                
                if positions:
                    for pos in positions:
                        # get_positions calculates valuation based on latest price if available
                        if pos.valuation is not None:
                            total_current_value += pos.valuation
                        elif pos.quantity > 0 and pos.avg_price > 0:
                            # Fallback if no current price (should rarely happen if price service works)
                           total_current_value += pos.quantity * pos.avg_price

                        total_invested += float(pos.quantity) * float(pos.avg_price)
                
                return_rate = 0.0
                if total_invested > 0:
                    return_rate = ((total_current_value - total_invested) / total_invested) * 100
                
                ranking_data.append({
                    "user_id": pf.owner_id,
                    "portfolio_id": pf.id,
                    "return_rate": return_rate,
                    "total_value": total_current_value
                })
            except Exception as e:
                logger.error(f"Error calculating ranking for portfolio {pf.id}: {e}")
                continue

        # Sort by return_rate descending
        ranking_data.sort(key=lambda x: x["return_rate"], reverse=True)

        # 2. Update DB
        try:
            # Delete existing DB ranks for this period
            stmt_del = select(LeaderboardRank).where(LeaderboardRank.period == period)
            result_del = await session.execute(stmt_del)
            existing_ranks = result_del.scalars().all()
            for r in existing_ranks:
                await session.delete(r)
            
            await session.flush()
            
            db_objects = []
            redis_mapping = {}
            redis_key = self._get_redis_key(period) # Defined here for use in Redis block

            for rank_idx, data in enumerate(ranking_data, 1):
                db_objects.append(LeaderboardRank(
                    user_id=data["user_id"],
                    portfolio_id=data["portfolio_id"],
                    period=period,
                    return_rate=data["return_rate"],
                    rank=rank_idx,
                    total_value=data["total_value"]
                ))
                redis_mapping[str(data["user_id"])] = data["return_rate"]

            if db_objects:
                session.add_all(db_objects)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

        # 3. Update Redis (Best Effort)
        if redis_mapping:
            try:
                redis_client = await get_redis_client()
                await redis_client.delete(redis_key)
                await redis_client.zadd(redis_key, redis_mapping)
            except Exception as e:
                logger.warning(f"Failed to update Redis leaderboard: {e}")
            
        return len(db_objects)

    async def get_top_n(self, n: int = 10, period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME, session: Optional[AsyncSession] = None) -> List[Tuple[int, float]]:
        """
        상위 N명 조회 (Redis 우선, DB fallback)
        """
        try:
            redis_client = await get_redis_client()
            redis_key = self._get_redis_key(period)
            
            # Check if key exists using exists() or just try range
            # zrevrange returns list of (member, score)
            results = await redis_client.zrevrange(redis_key, 0, n - 1, withscores=True)
            
            # If results empty, try DB fallback if session provided
            if not results and session:
                logger.info("Redis cache miss, fetching from DB")
                stmt = (
                    select(LeaderboardRank)
                    .where(LeaderboardRank.period == period)
                    .order_by(LeaderboardRank.rank)
                    .limit(n)
                )
                db_results = await session.execute(stmt)
                ranks = db_results.scalars().all()
                return [(r.user_id, r.return_rate) for r in ranks]

            return [(int(user_id), float(score)) for user_id, score in results]
            
        except Exception as e:
            logger.warning(f"Error fetching leaderboard: {e}")
            # Fallback to DB if session provided
            if session:
                stmt = (
                    select(LeaderboardRank)
                    .where(LeaderboardRank.period == period)
                    .order_by(LeaderboardRank.rank)
                    .limit(n)
                )
                try:
                    db_results = await session.execute(stmt)
                    ranks = db_results.scalars().all()
                    return [(r.user_id, r.return_rate) for r in ranks]
                except Exception as db_e:
                    logger.error(f"DB Fallback failed: {db_e}")
            return []

    async def get_user_rank(self, user_id: int, period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME) -> Optional[int]:
        """
        특정 사용자의 순위 조회 (1-based)
        """
        try:
            redis_client = await get_redis_client()
            redis_key = self._get_redis_key(period)
            rank = await redis_client.zrevrank(redis_key, str(user_id))
            return rank + 1 if rank is not None else None
        except Exception:
            # DB Fallback not implemented for simple rank check yet
            return None

leaderboard_service = LeaderboardService()
