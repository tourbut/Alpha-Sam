from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_

from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.models.position import Position
from app.src.schemas.asset import AssetCreate

async def get_assets(
    *, session: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Tuple[Asset, Optional[float], Optional[datetime], Optional[Position]]]:
    """
    Get assets with their latest price and associated first position for the specific user.
    Returns assets where owner_id is None (Global) OR matches owner_id (Private).
    """
    try:
        statement = select(Asset).where(
            or_(Asset.owner_id == None, Asset.owner_id == owner_id)
        ).offset(skip).limit(limit)
        result = await session.execute(statement)
        assets = result.scalars().all()
        
        asset_data = []
        for asset in assets:
            # Latest price
            price_stmt = select(Price).where(Price.asset_id == asset.id).order_by(desc(Price.timestamp)).limit(1)
            price_res = await session.execute(price_stmt)
            latest_price_obj = price_res.scalar_one_or_none()
            
            # Position for the specific user
            position_stmt = select(Position).where(
                Position.asset_id == asset.id,
                Position.owner_id == owner_id
            ).limit(1)
            position_res = await session.execute(position_stmt)
            position_obj = position_res.scalar_one_or_none()

            latest_price = latest_price_obj.value if latest_price_obj else None
            latest_timestamp = latest_price_obj.timestamp if latest_price_obj else None
            
            asset_data.append((asset, latest_price, latest_timestamp, position_obj))
            
        return asset_data
    except Exception as e:
        print(e)
        raise e

async def get_asset_by_symbol(*, session: AsyncSession, symbol: str) -> Optional[Asset]:
    try:
        statement = select(Asset).where(Asset.symbol == symbol)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    except Exception as e:
        print(e)
        raise e

async def get_asset(*, session: AsyncSession, asset_id: int) -> Optional[Asset]:
    try:
        return await session.get(Asset, asset_id)
    except Exception as e:
        print(e)
        raise e

async def create_asset(*, session: AsyncSession, obj_in: AssetCreate) -> Asset:
    try:
        db_obj = Asset.model_validate(obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def remove_asset(*, session: AsyncSession, asset_id: int) -> Optional[Asset]:
    try:
        obj = await session.get(Asset, asset_id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj
    except Exception as e:
        print(e)
        await session.rollback()
        raise e
