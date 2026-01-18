from datetime import datetime
from enum import Enum
import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint
from sqlalchemy import Column, DateTime, func

class UserFollow(SQLModel, table=True):
    """사용자 팔로우 관계 테이블"""
    __tablename__ = "user_follows"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    follower_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    following_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    
    __table_args__ = (
        # 동일한 팔로우 관계 중복 방지
        UniqueConstraint('follower_id', 'following_id', name='uq_user_follow'),
    )

class LeaderboardPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    ALL_TIME = "all_time"

class LeaderboardRank(SQLModel, table=True):
    """리더보드 랭킹 스냅샷 테이블"""
    __tablename__ = "leaderboard_ranks"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    portfolio_id: int = Field(foreign_key="portfolios.id", nullable=False)
    period: LeaderboardPeriod = Field(nullable=False, index=True)
    return_rate: float = Field(nullable=False)  # 수익률 (소수점, 예: 0.15 = 15%)
    rank: int = Field(nullable=False)           # 순위 (1부터 시작)
    total_value: float = Field(nullable=True)   # 총 평가금액 (선택)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )
    
    __table_args__ = (
        # 동일 기간에 유저당 하나의 랭킹만 존재
        UniqueConstraint('user_id', 'period', name='uq_leaderboard_user_period'),
    )
