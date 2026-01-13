"""
시세 업데이트 Celery 태스크
주기적으로 모든 자산의 시세를 업데이트
"""
import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

from app.celery_app import celery_app
from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.engine.price_service import price_service
from app.src.core.cache import cache_service
from app.src.core.db import engine, AsyncSessionLocal
import yfinance as yf


async def _update_all_prices_async() -> int:
    """
    모든 자산의 시세를 업데이트하는 비동기 함수
    
    Returns:
        업데이트된 자산 개수
    """
    async with AsyncSessionLocal() as session:
        # 1. 모든 자산 조회
        result = await session.execute(select(Asset))
        assets = result.scalars().all()
        
        updated_count = 0
        
        # 2. 각 자산별 시세 조회 및 저장
        for asset in assets:
            # [Refactor] 외부 API 호출을 생략하고 Redis에서만 최신 가격 조회
            current_price = await price_service.get_current_price(asset.symbol)
            
            new_price = Price(
                asset_id=asset.id,
                value=current_price,
                timestamp=datetime.utcnow()
            )
            
            session.add(new_price)
            updated_count += 1
            
            # Check for Price Alerts
            await price_service.check_and_trigger_alerts(asset.symbol, current_price, session=session)
        
        await session.commit()
        
        return updated_count


@celery_app.task(name="app.src.engine.tasks.price_tasks.update_all_prices")
def update_all_prices() -> dict:
    """
    모든 자산의 시세를 업데이트하는 Celery 태스크
    5분마다 Celery Beat에 의해 실행됨
    
    Returns:
        업데이트 결과 딕셔너리
    """
    try:
        # 비동기 함수를 동기 컨텍스트에서 실행
        updated_count = asyncio.run(_update_all_prices_async())
        return {
            "status": "success",
            "updated_count": updated_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@celery_app.task(name="app.src.engine.tasks.price_tasks.collect_market_prices")
def collect_market_prices() -> dict:
    """
    Yahoo Finance에서 시세를 가져와 Redis에 동기화하는 태스크
    """
    # 스크립트의 로직을 태스크로 구현
    SYMBOLS = {
        "BTC-USD": "BTC", "ETH-USD": "ETH", "SOL-USD": "SOL",
        "AAPL": "AAPL", "TSLA": "TSLA", "MSFT": "MSFT",
        "GOOGL": "GOOGL", "NVDA": "NVDA"
    }
    
    async def run_collect():
        results = {"success": 0, "failed": 0}
        for yf_symbol, app_symbol in SYMBOLS.items():
            def fetch():
                ticker = yf.Ticker(yf_symbol)
                try:
                    return ticker.fast_info['last_price']
                except:
                    try:
                        hist = ticker.history(period="1d")
                        return hist['Close'].iloc[-1] if not hist.empty else 0.0
                    except: return 0.0
            
            price = await asyncio.to_thread(fetch)
            if price > 0:
                cache_key = f"price:{app_symbol}"
                # 3분 TTL로 Redis 저장
                await cache_service.set(cache_key, str(price), ttl=180)
                results["success"] += 1
            else:
                results["failed"] += 1
        return results

    try:
        results = asyncio.run(run_collect())
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
