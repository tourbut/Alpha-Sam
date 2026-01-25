import asyncio
import logging
import yfinance as yf
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.admin import AdminAsset
from app.src.core.cache import cache_service

logger = logging.getLogger(__name__)

class PriceCollectorService:
    async def collect_active_assets(self, session: AsyncSession) -> dict:
        """
        Active 상태인 AdminAsset들의 시세를 수집하여 Redis에 캐싱
        """
        # 1. Active Asset 조회
        stmt = select(AdminAsset).where(AdminAsset.is_active == True)
        result = await session.execute(stmt)
        admin_assets = result.scalars().all()
        
        if not admin_assets:
            return {"status": "no_assets", "count": 0}

        results = {"success": 0, "failed": 0, "total": len(admin_assets)}

        # 2. 각 자산별 시세 수집 (비동기 병렬 처리 가능하나, 안정성을 위해 순차 처리 or 세마포어)
        # yfinance는 내부적으로 thread safe하지 않을 수 있음.
        
        for asset in admin_assets:
            try:
                price = await self._fetch_single_price(asset.symbol)
                if price > 0:
                    # Redis Cache Key: "price:{SYMBOL}"
                    # 대문자로 통일
                    symbol_key = asset.symbol.upper()
                    await cache_service.set(f"price:{symbol_key}", str(price), ttl=180)
                    results["success"] += 1
                else:
                    logger.warning(f"Failed to fetch price for {asset.symbol}")
                    results["failed"] += 1
            except Exception as e:
                logger.error(f"Error fetching {asset.symbol}: {e}")
                results["failed"] += 1
                
        return results

    async def _fetch_single_price(self, symbol: str) -> float:
        def fetch():
            ticker = yf.Ticker(symbol)
            try:
                return ticker.fast_info['last_price']
            except:
                try:
                    hist = ticker.history(period="1d")
                    return hist['Close'].iloc[-1] if not hist.empty else 0.0
                except:
                    return 0.0
        
        return await asyncio.to_thread(fetch)

price_collector = PriceCollectorService()
