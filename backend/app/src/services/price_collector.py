import asyncio
import logging
import yfinance as yf
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.admin import AdminAsset
from app.src.models.asset import Asset
from app.src.core.cache import cache_service

logger = logging.getLogger(__name__)

class PriceCollectorService:
    async def collect_active_assets(self, session: AsyncSession) -> dict:
        """
        Active 상태인 AdminAsset들과 사용자가 등록한 Asset들의 시세를 수집하여 Redis에 캐싱
        """
        # 1. AdminAsset (System Assets) 조회
        stmt_admin = select(AdminAsset).where(AdminAsset.is_active == True)
        result_admin = await session.execute(stmt_admin)
        admin_assets = result_admin.scalars().all()
        
        # 2. User Asset (User Portfolios) 조회 (Distinct Symbol)
        stmt_user = select(Asset.symbol).distinct()
        result_user = await session.execute(stmt_user)
        user_asset_symbols = result_user.scalars().all()
        
        # 3. 심볼 통합 및 중복 제거
        target_symbols = set()
        
        # Admin Asset 추가
        for asset in admin_assets:
            if asset.symbol:
                target_symbols.add(asset.symbol.upper())
                
        # User Asset 추가
        for symbol in user_asset_symbols:
            if symbol:
                target_symbols.add(symbol.upper())
        
        if not target_symbols:
            return {"status": "no_assets", "count": 0}

        results = {"success": 0, "failed": 0, "total": len(target_symbols)}

        # 4. 각 자산별 시세 수집
        for symbol in target_symbols:
            try:
                price = await self._fetch_single_price(symbol)
                if price > 0:
                    # Redis Cache Key: "price:{SYMBOL}"
                    await cache_service.set(f"price:{symbol}", str(price), ttl=600) # 10분 TTL matching Redis expiration policy
                    results["success"] += 1
                else:
                    logger.warning(f"Failed to fetch price for {symbol}")
                    results["failed"] += 1
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {e}")
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
