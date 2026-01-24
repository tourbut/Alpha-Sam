from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict

from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.services.price_service import price_service
from app.src.deps import SessionDep_async

router = APIRouter()

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_prices(
    session: SessionDep_async
) -> Dict[str, int]:
    """
    모든 자산의 시세를 최신화
    """
    try:
        # 1. 모든 자산 조회
        result = await session.execute(select(Asset))
        assets = result.scalars().all()
        
        updated_count = 0
        
        # 2. 각 자산별 시세 조회 및 저장 (캐시 무효화 후 조회)
        from datetime import datetime
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
        
        await session.commit()
        
        return {"updated_count": updated_count}
    except Exception as e:
        print(f"Error refreshing prices: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
