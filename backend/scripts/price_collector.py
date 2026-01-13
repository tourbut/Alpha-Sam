import asyncio
import os
import sys
import logging
import yfinance as yf

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.src.core.cache import cache_service

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PriceCollector")

# 수집 대상 심볼 (Yahoo Finance 필드 : 앱 내부 심볼)
# 앱 내부에서는 BTC, ETH 등으로 관리하고, 야후 파이낸스에서는 BTC-USD 등을 사용함
SYMBOLS = {
    "BTC-USD": "BTC",
    "ETH-USD": "ETH",
    "SOL-USD": "SOL",
    "AAPL": "AAPL",
    "TSLA": "TSLA",
    "MSFT": "MSFT",
    "GOOGL": "GOOGL",
    "NVDA": "NVDA"
}

CACHE_TTL = 300  # 5분 동안 캐시 유지

async def fetch_price(yf_symbol: str) -> float:
    """
    Yahoo Finance에서 단일 자산 가격 조회
    """
    def fetch():
        ticker = yf.Ticker(yf_symbol)
        try:
            # fast_info가 가장 빠르지만 실패할 경우 history 사용
            return ticker.fast_info['last_price']
        except Exception:
            try:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    return hist['Close'].iloc[-1]
            except Exception:
                pass
            return 0.0

    return await asyncio.to_thread(fetch)

async def collect_prices():
    """
    모든 심볼의 가격을 수집하고 Redis에 저장
    """
    logger.info("--- Starting Price Collection Cycle ---")
    
    for yf_symbol, app_symbol in SYMBOLS.items():
        price = await fetch_price(yf_symbol)
        
        if price > 0:
            cache_key = f"price:{app_symbol}"
            # Redis에 저장
            success = await cache_service.set(cache_key, str(price), ttl=CACHE_TTL)
            if success:
                logger.info(f"✅ [SUCCESS] {app_symbol}: {price:.2f}")
            else:
                logger.error(f"❌ [REDIS ERROR] Failed to save {app_symbol}")
        else:
            logger.warning(f"⚠️ [FETCH FAILED] {yf_symbol} returned 0.0")

    logger.info("--- Cycle Completed ---")

async def run_forever():
    """
    무한 루프로 주기적 실행 (1분 주기)
    """
    logger.info("🚀 Price Collector starting...")
    try:
        while True:
            await collect_prices()
            logger.info("Waiting 60 seconds for next cycle...")
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        logger.info("Price Collector main loop cancelled")

if __name__ == "__main__":
    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        logger.info("Stopped by user (Ctrl+C)")
    except Exception as e:
        logger.critical(f"Unexpected termination: {e}")
