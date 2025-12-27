from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.models.position import Position

async def get_position_by_asset(session: AsyncSession, asset_id: int, owner_id: int) -> Optional[Position]:
    statement = select(Position).where(
        Position.asset_id == asset_id,
        Position.owner_id == owner_id
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def create_position(session: AsyncSession, position_in: Position) -> Position:
    # Caution: Ensure position_in has owner_id set
    session.add(position_in)
    await session.commit()
    await session.refresh(position_in)
    return position_in

async def update_position_qty(session: AsyncSession, position: Position, new_quantity: float, new_avg_price: float) -> Position:
    position.quantity = new_quantity
    position.buy_price = new_avg_price
    # buy_date logic could be complex (e.g. FIFO), for now we keep the original or update to latest? 
    # Let's keep original buy_date for simplicity or update it if it was 0 qty.
    # We won't touch buy_date here for now unless necessary.
    
    session.add(position)
    await session.commit()
    await session.refresh(position)
    return position
