from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.src.core.db import get_session
from app.src.deps import get_current_user
from app.src.models.user import User
from app.src.models.portfolio_share import PortfolioShare
from app.src.schemas.social import PortfolioShareCreate, PortfolioShareRead, LeaderboardEntry
from app.src.services.leaderboard_service import leaderboard_service

router = APIRouter()

@router.post("/portfolio/share", response_model=PortfolioShareRead)
async def create_portfolio_share(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    share_in: PortfolioShareCreate
) -> Any:
    """
    사용자의 포트폴리오 공유 링크 생성
    """
    db_obj = PortfolioShare(
        user_id=current_user.id,
        settings=share_in.settings,
        is_active=share_in.is_active
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    *,
    session: AsyncSession = Depends(get_session),
    n: int = 10
) -> Any:
    """
    수익률 리더보드 조회 (Top N)
    """
    top_n = await leaderboard_service.get_top_n(n)
    
    leaderboard = []
    for rank, (user_id, pnl) in enumerate(top_n, 1):
        # 닉네임 조회를 위해 User 테이블 쿼리
        user = await session.get(User, user_id)
        nickname = user.nickname if user else f"User_{user_id}"
        
        leaderboard.append(
            LeaderboardEntry(
                user_id=user_id,
                nickname=nickname,
                pnl_percent=pnl,
                rank=rank
            )
        )
    
    return leaderboard
