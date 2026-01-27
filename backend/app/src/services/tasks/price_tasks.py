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
from app.src.services.price_service import price_service
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


@celery_app.task(name="app.src.services.tasks.price_tasks.update_all_prices")
def update_all_prices() -> dict:
    """
    모든 자산의 시세를 업데이트하는 Celery 태스크
    5분마다 Celery Beat에 의해 실행됨
    """
    from sqlalchemy.pool import NullPool
    from app.src.core.db import settings
    
    # Celery Task마다 새로운 Event Loop가 생성되므로(asyncio.run),
    # Global Engine(Pooling)을 사용하면 Loop 불일치로 인한 asyncpg 에러 발생 가능.
    # 따라서 Task 내부에서 NullPool을 사용하는 전용 Engine을 생성하여 사용.
    
    async def run_update():
        # Task 전용 엔진 생성 (Connection Pooling 미사용)
        task_engine = create_async_engine(
            settings.database_url,
            poolclass=NullPool,
            echo=True, # For debugging
        )
        TaskSessionLocal = async_sessionmaker(task_engine, class_=AsyncSession, expire_on_commit=False)
        
        try:
            async with TaskSessionLocal() as session:
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
        finally:
             await task_engine.dispose()

    try:
        updated_count = asyncio.run(run_update())
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


@celery_app.task(name="app.src.services.tasks.price_tasks.collect_market_prices")
def collect_market_prices() -> dict:
    """
    관심 종목(AdminAsset)의 시세를 가져와 Redis에 동기화하는 태스크
    """
    from app.src.services.price_collector import price_collector
    from sqlalchemy.pool import NullPool
    from app.src.core.db import settings
    
    async def run_collect():
        # Task 전용 엔진 생성 (Connection Pooling 미사용)
        task_engine = create_async_engine(
            settings.database_url,
            poolclass=NullPool,
            # echo=True,
        )
        TaskSessionLocal = async_sessionmaker(task_engine, class_=AsyncSession, expire_on_commit=False)
        
        try:
            async with TaskSessionLocal() as session:
                return await price_collector.collect_active_assets(session)
        finally:
            await task_engine.dispose()

    try:
        results = asyncio.run(run_collect())
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
