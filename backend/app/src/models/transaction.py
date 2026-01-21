"""
Transaction (거래 내역) 모델
"""
import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, String, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from app.src.models.asset import Asset
    from app.src.models.portfolio import Portfolio

class Transaction(SQLModel, table=True):
    """
    거래 내역 모델
    
    Attributes:
        id: 거래 고유 ID
        portfolio_id: 포트폴리오 ID
        asset_id: 자산 ID
        type: 거래 유형 (BUY / SELL)
        quantity: 거래 수량
        price: 거래 단가
        timestamp: 거래 시각 (executed_at)
    """
    __tablename__ = "transactions"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    portfolio_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True),
        description="포트폴리오 ID"
    )
    asset_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True),
        description="자산 ID"
    )
    type: str = Field(
        sa_column=Column(String(10)),
        description="거래 유형 (BUY/SELL)"
    )
    quantity: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="거래 수량"
    )
    price: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="거래 단가"
    )
    executed_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="거래 체결 시각"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    
    # Relationship
    portfolio: "Portfolio" = Relationship(back_populates="transactions")
    asset: "Asset" = Relationship(back_populates="transactions")
