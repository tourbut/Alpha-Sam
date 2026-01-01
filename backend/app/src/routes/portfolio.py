from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.db import get_session
from app.src.schemas.portfolio import PortfolioResponse, PortfolioHistoryRead
from app.src.deps import get_current_user
from app.src.models.user import User

router = APIRouter()


@router.post("/snapshot", status_code=status.HTTP_201_CREATED)
async def create_portfolio_snapshot(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    현재 포트폴리오 가치 스냅샷 생성 및 저장
    """
    from app.src.services.portfolio_service import PortfolioService
    history = await PortfolioService.create_snapshot(session, current_user.id)
    return {"message": "Snapshot created", "data": history}


@router.get("/summary", response_model=PortfolioResponse)
async def get_portfolio_summary(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포트폴리오 요약 정보 및 전체 포지션 현황 조회
    """
    from app.src.services.portfolio_service import PortfolioService
    return await PortfolioService.get_summary(session, current_user.id)


@router.get("/history", response_model=List[PortfolioHistoryRead])
async def read_portfolio_history(
    skip: int = 0,
    limit: int = 30,  # Default to 30 for chart
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포트폴리오 히스토리 조회
    """
    # History read is simple CRUD, might stay here or move to service later if logic grows
    from app.src.crud import crud_portfolio_history
    return await crud_portfolio_history.get_portfolio_history(session, owner_id=current_user.id, skip=skip, limit=limit)
