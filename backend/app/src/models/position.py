"""
Position (보유 내역) 모델
특정 자산에 대한 사용자의 보유 상태를 나타냄
"""
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, Date, func, ForeignKey, CheckConstraint, UniqueConstraint


class Position(SQLModel, table=True):
    """
    보유 내역 모델
    
    Attributes:
        id: 포지션 고유 ID (자동 생성)
        asset_id: 자산 ID (Asset 참조)
        quantity: 보유 수량 (0 이상, 음수 불가)
        buy_price: 매수 단가 (0 초과)
        buy_date: 매수 일자 (선택적)
        created_at: 생성 시각
        updated_at: 수정 시각
    """
    __tablename__ = "positions"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_non_negative"),
        CheckConstraint("buy_price > 0", name="check_buy_price_positive"),
        UniqueConstraint("owner_id", "asset_id", name="uq_position_owner_asset"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(
        foreign_key="assets.id",
        index=True,
        description="자산 ID"
    )
    owner_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="소유자 User ID"
    )
    quantity: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        ge=0.0,
        description="보유 수량 (0 이상)"
    )
    buy_price: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        gt=0.0,
        description="매수 단가 (0 초과)"
    )
    buy_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date),
        description="매수 일자 (선택적)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    # Relationship
    asset: Optional["Asset"] = Relationship(back_populates="positions")

