from datetime import datetime
import uuid
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from sqlalchemy import Column, DateTime, String, func, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from app.src.models.user import User
    from app.src.models.portfolio import Portfolio

class UserFollow(SQLModel, table=True):
    """사용자 팔로우 관계 테이블"""
    __tablename__ = "user_follows"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    follower_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True),
    )
    following_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True),
    )
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
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True),
        description="평가 참여자 ID"
    )
    portfolio_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False),
        description="대상 포트폴리오 ID"
    )
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
