from typing import List, Optional
import uuid
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.models.transaction import Transaction

async def create_portfolio(
    *, session: AsyncSession, owner_id: uuid.UUID, name: str, description: Optional[str] = None
) -> Portfolio:
    portfolio = Portfolio(owner_id=owner_id, name=name, description=description)
    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)
    return portfolio

async def get_user_portfolios(*, session: AsyncSession, owner_id: uuid.UUID) -> List[Portfolio]:
    stmt = select(Portfolio).where(Portfolio.owner_id == owner_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_recent_portfolios(
    *, session: AsyncSession, owner_id: uuid.UUID, limit: int = 5
) -> List[Portfolio]:
    stmt = (
        select(Portfolio)
        .where(Portfolio.owner_id == owner_id)
        .order_by(desc(Portfolio.created_at))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_portfolio(
    *, session: AsyncSession, portfolio_id: uuid.UUID, owner_id: Optional[uuid.UUID] = None
) -> Optional[Portfolio]:
    stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
    if owner_id:
        stmt = stmt.where(Portfolio.owner_id == owner_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_shared_portfolio(*, session: AsyncSession, token: uuid.UUID) -> Optional[Portfolio]:
    stmt = select(Portfolio).where(Portfolio.share_token == token)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def update_visibility(
    *, session: AsyncSession, portfolio_id: uuid.UUID, visibility: PortfolioVisibility
) -> Optional[Portfolio]:
    stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
    result = await session.execute(stmt)
    portfolio = result.scalar_one_or_none()
        
    if not portfolio:
        return None
            
    portfolio.visibility = visibility
        
    if visibility == PortfolioVisibility.LINK_ONLY:
        if not portfolio.share_token:
            portfolio.share_token = uuid.uuid4()
    elif visibility == PortfolioVisibility.PRIVATE:
        portfolio.share_token = None
            
    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)
    return portfolio

async def add_transaction(
    *, 
    session: AsyncSession, 
    portfolio_id: uuid.UUID, 
    asset_id: uuid.UUID, 
    type: str, 
    quantity: float, 
    price: float, 
    executed_at
) -> Transaction:
    tx = Transaction(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        type=type,
        quantity=quantity,
        price=price,
        executed_at=executed_at
    )
    session.add(tx)
    await session.commit()
    await session.refresh(tx)
    return tx
