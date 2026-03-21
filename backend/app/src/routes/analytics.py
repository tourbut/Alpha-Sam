import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.schemas.analytics import AssetAllocationResponse, PortfolioHistoryResponse
from app.src.services import analytics_service
from app.src.deps import SessionDep_async, CurrentUser
from app.src.models.portfolio import Portfolio

router = APIRouter()

async def check_portfolio_ownership(session: AsyncSession, portfolio_id: uuid.UUID, user_id: uuid.UUID):
    portfolio = await session.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return portfolio

@router.get("/portfolio/{portfolio_id}/allocation", response_model=List[AssetAllocationResponse])
async def get_allocation(*, 
    portfolio_id: uuid.UUID,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    Get asset allocation for a specific portfolio (Pie chart data)
    """
    await check_portfolio_ownership(session, portfolio_id, current_user.id)
    allocations = await analytics_service.get_portfolio_allocation(session, portfolio_id)
    return allocations

@router.get("/portfolio/{portfolio_id}/history", response_model=List[PortfolioHistoryResponse])
async def get_history(*, 
    portfolio_id: uuid.UUID,
    session: SessionDep_async,
    current_user: CurrentUser,
    range: str = Query("1M", regex="^(1W|1M|1Y|YTD|ALL)$")
):
    """
    Get portfolio value history (Line chart data)
    """
    await check_portfolio_ownership(session, portfolio_id, current_user.id)
    history = await analytics_service.get_portfolio_history(session, portfolio_id, range=range)
    return history

@router.get("/portfolios/allocation", response_model=List[AssetAllocationResponse])
async def get_portfolios_allocation(*, 
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    Get aggregated asset allocation across all portfolios for the current user
    """
    allocations = await analytics_service.get_portfolios_allocation(session, current_user.id)
    return allocations

@router.get("/portfolios/history", response_model=List[PortfolioHistoryResponse])
async def get_portfolios_history(*, 
    session: SessionDep_async,
    current_user: CurrentUser,
    range: str = Query("1M", regex="^(1W|1M|1Y|YTD|ALL)$")
):
    """
    Get aggregated portfolio value history across all portfolios for the current user
    """
    history = await analytics_service.get_portfolios_history(session, current_user.id, range=range)
    return history
