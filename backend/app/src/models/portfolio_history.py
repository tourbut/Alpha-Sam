"""
PortfolioHistory (포트폴리오 히스토리) 모델
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class PortfolioHistory(SQLModel, table=True):
    """
    포트폴리오 과거 이력 모델 (Snapshot)
    
    Attributes:
        id: ID
        total_value: 총 평가금액
        total_cost: 총 매수금액
        total_pl: 총 손익
        timestamp: 기록 시각
    """
    __tablename__ = "portfolio_history"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    owner_id: Optional[uuid.UUID] = Field(
        default=None, 
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id")),
        description="Owner User ID"
    )
    total_value: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="총 평가금액"
    )
    total_cost: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="총 매수금액"
    )
    total_pl: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="총 손익"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), index=True),
        description="기록 시각"
    )
