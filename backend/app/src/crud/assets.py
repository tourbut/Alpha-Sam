import uuid
from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_

from app.src.models.asset import Asset
from app.src.models.price import Price

from app.src.schemas.asset import AssetCreate

async def get_assets(
    *, session: AsyncSession, owner_id: uuid.UUID, portfolio_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 100
) -> List[Asset]:
    """
    Get assets with their latest price for the specific user.
    Returns assets where owner_id is None (Global) OR matches owner_id (Private).
    
    참고: Position 정보는 더 이상 여기서 반환하지 않음.
    Position은 Transaction을 집계하여 동적으로 계산됨.
    """
    try:
        statement = select(Asset).where(
            Asset.owner_id == owner_id
        )
        if portfolio_id:
            statement = statement.where(Asset.portfolio_id == portfolio_id)
            
        statement = statement.offset(skip).limit(limit)
    
        result = await session.execute(statement)
        assets = result.scalars().all()
            
        return assets
    except Exception as e:
        print(e)
        raise e

async def get_asset_by_symbol(*, session: AsyncSession, symbol: str, owner_id: Optional[uuid.UUID] = None, portfolio_id: Optional[uuid.UUID] = None) -> Optional[Asset]:
    try:
        if owner_id is not None:
             statement = select(Asset).where(
                 Asset.symbol == symbol,
                 Asset.owner_id == owner_id
             )
             if portfolio_id:
                 statement = statement.where(Asset.portfolio_id == portfolio_id)
        else:
            statement = select(Asset).where(Asset.symbol == symbol)
            
        result = await session.execute(statement)
        # Use first() to avoid MultipleResultsFound error if data integrity was compromised or concurrent creates happen
        return result.scalars().first()
    except Exception as e:
        print(e)
        raise e

async def get_asset(*, session: AsyncSession, asset_id: uuid.UUID) -> Optional[Asset]:
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

async def remove_asset(*, session: AsyncSession, asset_id: uuid.UUID) -> Optional[Asset]:
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

async def get_recent_assets(
    *, session: AsyncSession, owner_id: uuid.UUID, limit: int = 5
) -> List[Asset]:
    try:
        stmt = (
            select(Asset)
            .where(Asset.owner_id == owner_id)
            .order_by(desc(Asset.created_at))
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(e)
        raise e
