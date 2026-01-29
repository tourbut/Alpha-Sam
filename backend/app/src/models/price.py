"""
PriceDay (일봉 시세) 모델
yfinance의 일봉 데이터(OHLCV)를 저장
"""
import uuid
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Date, Numeric, BigInteger, func, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class PriceDay(SQLModel, table=True):
    """
    일봉 시세 정보 모델 (OHLCV)
    
    Attributes:
        id: 고유 ID
        asset_id: 자산 ID
        date: 기준 일자
        open: 시가
        high: 고가
        low: 저가
        close: 종가
        volume: 거래량
        adjusted_close: 수정 종가
    """
    __tablename__ = "prices_day"
    __table_args__ = (
        UniqueConstraint("asset_id", "date", name="uq_prices_day_asset_date"),
    )
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    asset_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True),
        description="자산 ID"
    )
    date: date = Field(
        sa_column=Column(Date, nullable=False, index=True),
        description="기준 일자"
    )
    open: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="시가"
    )
    high: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="고가"
    )
    low: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="저가"
    )
    close: float = Field(
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="종가"
    )
    volume: int = Field(
        sa_column=Column(BigInteger),
        description="거래량"
    )
    adjusted_close: Optional[float] = Field(
        default=None,
        sa_column=Column(Numeric(precision=20, scale=8)),
        description="수정 종가"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    
    # Relationship
    asset: Optional["Asset"] = Relationship(back_populates="price_days")
