import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, func, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from app.src.models.portfolio import Portfolio
    from app.src.models.asset import Asset

class Position(SQLModel, table=True):
    """
    Position (보유 내역) 모델 - Materialized View 성격
    Transaction 기반으로 실시간 갱신되지만,
    조회 성능을 위해 DB에 물리적으로 저장됨.
    """
    __tablename__ = "positions"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    portfolio_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True)
    )
    asset_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    )
    
    quantity: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8), nullable=False, default=0)
    )
    avg_price: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8), nullable=False, default=0),
        description="평균 매입 단가 (이동평균법 등 적용)"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    __table_args__ = (
        UniqueConstraint('portfolio_id', 'asset_id', name='uq_position_portfolio_asset'),
    )

    # Relationships
    portfolio: "Portfolio" = Relationship(back_populates="positions")
    asset: "Asset" = Relationship(back_populates="positions")
