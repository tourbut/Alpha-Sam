"""
Price (시세) 모델
외부 데이터 소스에서 가져오는 현재 단가 정보
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Price(SQLModel, table=True):
    """
    시세 정보 모델
    
    Attributes:
        id: 시세 고유 ID (자동 생성)
        asset_id: 자산 ID (Asset 참조)
        value: 현재 가격
        timestamp: 시세 기준 시각
        created_at: 레코드 생성 시각
    """
    __tablename__ = "prices"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    asset_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True),
        description="자산 ID"
    )
    value: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="현재 가격"
    )
    timestamp: datetime = Field(
        description="시세 기준 시각"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    
    # Relationship
    asset: Optional["Asset"] = Relationship(back_populates="prices")



