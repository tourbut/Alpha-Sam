"""
Transaction (거래 내역) 모델
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Numeric, String, func

class Transaction(SQLModel, table=True):
    """
    거래 내역 모델
    
    Attributes:
        id: 거래 고유 ID
        asset_id: 자산 ID
        type: 거래 유형 (BUY / SELL)
        quantity: 거래 수량
        price: 거래 단가
        timestamp: 거래 시각
    """
    __tablename__ = "transactions"
    
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
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="거래 시각"
    )
    
    # Relationship
    asset: Optional["Asset"] = Relationship(back_populates="transactions")
