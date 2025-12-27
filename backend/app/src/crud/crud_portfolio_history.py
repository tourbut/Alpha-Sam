"""
Portfolio History CRUD
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.src.models.portfolio_history import PortfolioHistory

async def create_portfolio_history(session: AsyncSession, history: PortfolioHistory) -> PortfolioHistory:
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return history

async def get_portfolio_history(
    session: AsyncSession,
    owner_id: int,
    skip: int = 0, 
    limit: int = 100
) -> List[PortfolioHistory]:
    stmt = select(PortfolioHistory).where(PortfolioHistory.owner_id == owner_id).order_by(desc(PortfolioHistory.timestamp)).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
