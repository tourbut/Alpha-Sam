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
from app.src.core.db import engine, AsyncSessionLocal


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
            # 캐시 무효화
            await price_service.invalidate_cache(asset.symbol)
            
            # 캐시를 사용하지 않고 최신 가격 조회
            current_price = await price_service.get_current_price(asset.symbol, use_cache=False)
            
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

