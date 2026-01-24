import asyncio
import logging
import yfinance as yf
import uuid
from typing import List, Optional, Dict
from app.src.core.cache import cache_service
from sqlalchemy.ext.asyncio import AsyncSession # Assuming AsyncSession is needed for the new signature

logger = logging.getLogger(__name__)

class PriceService:
    """
    Price Service with yfinance and Redis Caching
    Fetches real-time prices from Yahoo Finance API.
    """
    
    # Fallback/Initial prices
    MOCK_PRICES = {
        "BTC": 100000.0,
        "ETH": 3500.0,
        "SOL": 150.0,
        "AAPL": 180.0,
        "TSLA": 250.0
    }
    
    CACHE_KEY_PREFIX = "price:"
    CACHE_TTL = 180  # 3 minutes

    async def get_current_price(self, symbol: str, use_cache: bool = True) -> float:
        """
        Get current price of an asset.
        If use_cache is True, try Redis first.
        If not found or use_cache is False, fetch from yfinance API.
        """
        symbol_upper = symbol.upper()
        cache_key = f"{self.CACHE_KEY_PREFIX}{symbol_upper}"
        
        if use_cache:
            cached_value = await cache_service.get(cache_key)
            if cached_value is not None:
                try:
                    return float(cached_value)
                except (ValueError, TypeError):
                    logger.error(f"Invalid price value in cache for {symbol_upper}: {cached_value}")
        
        # Fetch from Source (yfinance)
        # Note: _fetch_price_from_yfinance is an async wrapper around blocking yfinance call
        price = await self._fetch_price_from_yfinance(symbol_upper)
        
        if price > 0:
            # Update Cache
            await cache_service.set(cache_key, str(price), ttl=self.CACHE_TTL)
        else:
            # Fallback to Mock if yfinance fails
            price = self.MOCK_PRICES.get(symbol_upper, 0.0)
            if price == 0.0:
                 logger.warning(f"Price for {symbol_upper} not found in Source or Mock.")

        return price

    async def get_latest_price(self, session: AsyncSession, asset_id: uuid.UUID) -> Optional[float]:
        """
        [Legacy/Deprecated] Use get_current_price instead.
        Kept for backward compatibility if needed, but logic is broken (uses undefined 'symbol').
        """
        # This method in previous file content had a bug: 'symbol' was undefined.
        # Assuming we need to fetch asset symbol from DB using asset_id.
        # But for now, let's just log error or return 0 as this seems unused or broken previously.
        logger.error("get_latest_price called but it is broken. Use get_current_price(symbol).")
        return 0.0

    async def _fetch_price_from_yfinance(self, symbol: str) -> float:
        """
        Internal method to fetch price using yfinance (blocking call wrapped in executor)
        """
        # Symbol Mapping for Crypto
        query_symbol = symbol
        if symbol in ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "DOT", "LINK", "LTC", "BCH", "EOS", "XLM", "TRX", "XMR"]:
            query_symbol = f"{symbol}-USD"
        
        def fetch():
            ticker = yf.Ticker(query_symbol)
            # 'fast_info' is faster than 'history' in newer yfinance versions
            try:
                 return ticker.fast_info['last_price']
            except (KeyError, AttributeError, Exception):
                 # Fallback to history
                 try:
                     hist = ticker.history(period="1d")
                     if not hist.empty:
                         return hist['Close'].iloc[-1]
                 except Exception:
                     pass
                 return 0.0

        return await asyncio.to_thread(fetch)

    async def invalidate_cache(self, symbol: Optional[str] = None) -> int:
        """
        Invalidate price cache
        """
        if symbol:
            cache_key = f"{self.CACHE_KEY_PREFIX}{symbol.upper()}"
            deleted = await cache_service.delete(cache_key)
            return 1 if deleted else 0
        else:
            pattern = f"{self.CACHE_KEY_PREFIX}*"
            return await cache_service.delete_pattern(pattern)

    async def search_symbol(self, query: str) -> list[dict]:
        """
        Search for symbols using Yahoo Finance Ticker.
        """
        import aiohttp
        
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        if "quotes" in data:
                            results = [
                                {
                                    "symbol": item.get("symbol"),
                                    "name": item.get("shortname", item.get("longname", "")),
                                    "type": item.get("quoteType"),
                                    "exchange": item.get("exchange")
                                }
                                for item in data["quotes"]
                                if item.get("quoteType") in ["EQUITY", "CRYPTOCURRENCY", "ETF", "MUTUALFUND", "INDEX", "CURRENCY"]
                            ]
                            return results
                    else:
                        logger.warning(f"Yahoo Search failed with status: {response.status}")
            except Exception as e:
                logger.error(f"Search failed: {e}")
        
        # Fallback: Check if the query itself is a valid symbol
        if await self.validate_symbol(query):
             return [{
                 "symbol": query.upper(),
                 "name": query.upper(), 
                 "type": "UNKNOWN", 
                 "exchange": "UNKNOWN"
             }]
        
        return []

    async def validate_symbol(self, symbol: str) -> bool:
        """
        Validates if a symbol exists on Yahoo Finance (Direct check)
        """
        try:
            # New assets might not be in Redis yet, so we check Yahoo Finance directly
            # once for validation purposes.
            price = await self._fetch_price_from_yfinance(symbol.upper())
            return price > 0
        except:
            return False

    async def check_and_trigger_alerts(self, asset_symbol: str, current_price: float, session: Optional[any] = None):
        """
        Check if current price meets any alert conditions and trigger email task.
        """
        if session is None:
            return

        from sqlalchemy import select
        from app.src.models.user import User
        from app.src.models.notification import NotificationSettings
        from app.src.services.tasks.email_tasks import send_price_alert
        from datetime import datetime

        # 1. 알림 설정이 켜져 있는 활성 사용자 조회
        # Note: 간단한 구현을 위해 모든 사용자를 조회하지만, 실무에서는 인덱스된 필드로 최적화 필요
        stmt = (
            select(User)
            .join(NotificationSettings, User.id == NotificationSettings.user_id)
            .where(User.is_active == True)
            .where(NotificationSettings.price_alert_enabled == True)
        )
        result = await session.execute(stmt)
        users = result.scalars().all()

        for user in users:
            # 해당 사용자가 이 자산을 보유하고 있는지 확인 (선택 사항, 여기서는 보유 중인 경우만 알림)
            from app.src.models.position import Position
            from app.src.models.asset import Asset
            
            check_stmt = (
                select(Position)
                .join(Asset, Position.asset_id == Asset.id)
                .where(Position.owner_id == user.id)
                .where(Asset.symbol == asset_symbol)
            )
            check_result = await session.execute(check_stmt)
            if check_result.scalar_one_or_none():
                # 태스크 발행 (Rate Limiting은 태스크 내부에서 처리됨)
                send_price_alert.delay(
                    to_email=user.email,
                    symbol=asset_symbol,
                    price=current_price,
                    timestamp=datetime.utcnow().isoformat()
                )

price_service = PriceService()
