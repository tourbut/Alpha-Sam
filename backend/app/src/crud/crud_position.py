import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.models.position import Position

async def get_position_by_asset(*, session: AsyncSession, asset_id: uuid.UUID, owner_id: uuid.UUID) -> Optional[Position]:
    try:
        statement = select(Position).where(
            Position.asset_id == asset_id,
            Position.owner_id == owner_id
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    except Exception as e:
        print(e)
        raise e

async def create_position(*, session: AsyncSession, position_in: Position) -> Position:
    # Caution: Ensure position_in has owner_id set
    try:
        session.add(position_in)
        await session.commit()
        await session.refresh(position_in)
        return position_in
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def update_position_qty(*, session: AsyncSession, position: Position, new_quantity: float, new_avg_price: float) -> Position:
    try:
        position.quantity = new_quantity
        position.buy_price = new_avg_price
        # buy_date logic could be complex (e.g. FIFO), for now we keep the original or update to latest? 
        # Let's keep original buy_date for simplicity or update it if it was 0 qty.
        # We won't touch buy_date here for now unless necessary.
        
        session.add(position)
        await session.commit()
        await session.refresh(position)
        return position
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def get_positions(*, session: AsyncSession, owner_id: uuid.UUID) -> List[Position]:
    try:
        stmt = select(Position).where(Position.owner_id == owner_id)
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(e)
        raise e

async def get_position(*, session: AsyncSession, position_id: uuid.UUID, owner_id: uuid.UUID) -> Optional[Position]:
    try:
        stmt = select(Position).where(
            Position.id == position_id,
            Position.owner_id == owner_id
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        print(e)
        raise e

async def update_position(*, session: AsyncSession, position: Position, update_data: dict) -> Position:
    try:
        for field, value in update_data.items():
            setattr(position, field, value)
        session.add(position)
        await session.commit()
        await session.refresh(position)
        return position
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def remove_position(*, session: AsyncSession, position: Position) -> None:
    try:
        await session.delete(position)
        await session.commit()
    except Exception as e:
        print(e)
        await session.rollback()
        raise e
