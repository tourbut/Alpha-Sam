from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.exc import IntegrityError

from app.src.core.db import get_session
from app.src.deps import SessionDep_async, CurrentUser
from app.src.models.user import User
from app.src.models.social import UserFollow, LeaderboardPeriod
from app.src.schemas.social import LeaderboardEntry, FollowerResponse, FollowListResponse, UserProfile
from app.src.services.leaderboard_service import leaderboard_service

router = APIRouter()

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    session: SessionDep_async,
    n: int = 10
) -> Any:
    """
    수익률 리더보드 조회 (Top N)
    """
    # 1. Get Top N from Service (Redis -> DB)
    top_n_tuples = await leaderboard_service.get_top_n(n, LeaderboardPeriod.ALL_TIME, session)
    
    leaderboard = []
    
    # 2. Add extra info (nickname, total_value from DB if needed)
    # Service get_top_n returns (user_id, return_rate)
    # We might need total_value too if we want to show it.
    # Current Redis get_top_n only stores score=return_rate.
    # To get total_value, we need to query LeaderboardRank table or just return 0 for now if Redis used.
    # For robust implementation, lets query User table for nicknames.
    
    for rank, (user_id, return_rate) in enumerate(top_n_tuples, 1):
        user = await session.get(User, user_id)
        if not user:
            continue
            
        # Try to find total_value from LeaderboardRank table for accuracy? 
        # Or Just Mock it/Leave 0. 
        # Let's query LeaderboardRank to get accurate total_value if possible, 
        # but that defeats the purpose of Redis speed.
        # Alternatively, assume we only show return_rate.
        # But schema requires total_value.
        # Let's fetch from LeaderboardRank table by user_id & period
        from app.src.models.social import LeaderboardRank
        stmt = select(LeaderboardRank).where(
            LeaderboardRank.user_id == user_id, 
            LeaderboardRank.period == LeaderboardPeriod.ALL_TIME
        )
        res = await session.execute(stmt)
        rank_obj = res.scalar_one_or_none()
        total_value = rank_obj.total_value if rank_obj else 0.0

        leaderboard.append(
            LeaderboardEntry(
                user_id=user_id,
                nickname=user.nickname or f"User_{user_id}",
                return_rate=return_rate,
                total_value=total_value,
                rank=rank
            )
        )
    
    return leaderboard

@router.post("/leaderboard/calculate", status_code=status.HTTP_202_ACCEPTED)
async def calculate_leaderboard_manually(
    session: SessionDep_async,
    # Admin only check in real app
):
    """
    [Dev/Admin] 리더보드 계산 수동 트리거
    """
    count = await leaderboard_service.calculate_leaderboard(session)
    return {"message": "Leaderboard calculation triggered", "updated_count": count}

@router.post("/follow/{target_id}", response_model=FollowerResponse, status_code=status.HTTP_201_CREATED)
async def follow_user(
    target_id: int,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    사용자 팔로우
    """
    if target_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    target_user = await session.get(User, target_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        follow = UserFollow(follower_id=current_user.id, following_id=target_id)
        session.add(follow)
        await session.commit()
        await session.refresh(follow)
        return follow
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Already following this user")

@router.delete("/follow/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    target_id: int,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    사용자 언팔로우
    """
    stmt = delete(UserFollow).where(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == target_id
    )
    result = await session.execute(stmt)
    await session.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Follow relationship not found")

@router.get("/users/{user_id}/followers", response_model=FollowListResponse)
async def get_followers(
    user_id: int,
    session: SessionDep_async,
    skip: int = 0, 
    limit: int = 20
):
    """
    특정 사용자의 팔로워 목록 조회
    """
    stmt = (
        select(User)
        .join(UserFollow, UserFollow.follower_id == User.id)
        .where(UserFollow.following_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    followers = result.scalars().all()
    
    # Count total
    count_stmt = select(func.count()).select_from(UserFollow).where(UserFollow.following_id == user_id)
    count_res = await session.execute(count_stmt)
    total = count_res.scalar()
    
    return FollowListResponse(
        total=total,
        users=[UserProfile(id=u.id, nickname=u.nickname, email=u.email) for u in followers]
    )

@router.get("/users/{user_id}/following", response_model=FollowListResponse)
async def get_following(
    user_id: int,
    session: SessionDep_async,
    skip: int = 0, 
    limit: int = 20
):
    """
    특정 사용자의 팔로잉 목록 조회
    """
    stmt = (
        select(User)
        .join(UserFollow, UserFollow.following_id == User.id)
        .where(UserFollow.follower_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    following = result.scalars().all()
    
    # Count total
    count_stmt = select(func.count()).select_from(UserFollow).where(UserFollow.follower_id == user_id)
    count_res = await session.execute(count_stmt)
    total = count_res.scalar()
    
    return FollowListResponse(
        total=total,
        users=[UserProfile(id=u.id, nickname=u.nickname, email=u.email) for u in following]
    )
