"""
Position (보유 내역) 모델
특정 포트폴리오 내 자산의 보유 상태를 나타냄 (Computed Snapshot)
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, func, CheckConstraint, UniqueConstraint

if TYPE_CHECKING:
    from app.src.models.asset import Asset
    from app.src.models.portfolio import Portfolio
    from app.src.models.transaction import Transaction

class Position(SQLModel, table=True):
    """
    보유 내역 모델 (Snapshot)
    Transaction 이력에 의해 자동 계산됨.
    
    Attributes:
        id: ID
        portfolio_id: 포트폴리오 ID
        asset_id: 자산 ID
        quantity: 보유 수량
        avg_price: 평단가
        last_transaction_id: 마지막으로 반영된 트랜잭션 ID
    """
    __tablename__ = "positions"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_non_negative"),
        UniqueConstraint("portfolio_id", "asset_id", name="uq_position_portfolio_asset"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(
        foreign_key="portfolios.id",
        index=True,
        description="포트폴리오 ID"
    )
    asset_id: int = Field(
        foreign_key="assets.id",
        index=True,
        description="자산 ID"
    )
    quantity: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        ge=0.0,
        description="보유 수량 (0 이상)"
    )
    avg_price: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        ge=0.0,
        description="평단가"
    )
    last_transaction_id: Optional[int] = Field(
        default=None,
        foreign_key="transactions.id",
        description="마지막 반영된 트랜잭션 ID (Sync 확인용)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    # Relationships
    portfolio: "Portfolio" = Relationship(back_populates="positions")
    asset: "Asset" = Relationship(back_populates="positions")

