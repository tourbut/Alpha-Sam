import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    from app.src.models.price import Price
    from app.src.models.transaction import Transaction
    from app.src.models.position import Position
    from app.src.models.portfolio import Portfolio

class Asset(SQLModel, table=True):
    """
    자산 정보 모델
    
    Attributes:
        id: 자산 고유 ID (자동 생성)
        symbol: 자산 심볼 (예: BTC, AAPL) - 대문자 추천
        name: 사람 친화적인 이름 (예: Bitcoin, Apple Inc.)
        category: 자산 카테고리 (코인, 주식, ETF 등) - 선택적
        created_at: 생성 시각
        updated_at: 수정 시각
    """
    __tablename__ = "assets"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    portfolio_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True),
        description="귀속 포트폴리오 ID"
    )
    owner_id: Optional[uuid.UUID] = Field(
        default=None, 
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
        description="Owner User ID"
    )
    symbol: str = Field(
        max_length=20,
        index=True,
        description="자산 심볼 (예: BTC, AAPL)"
    )
    name: str = Field(
        max_length=200,
        description="자산 이름"
    )
    category: Optional[str] = Field(
        default=None,
        max_length=50,
        description="자산 카테고리 (코인, 주식, ETF 등)"
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
    portfolio: Optional["Portfolio"] = Relationship(back_populates="assets")
    prices: List["Price"] = Relationship(back_populates="asset")
    transactions: List["Transaction"] = Relationship(back_populates="asset")
    positions: List["Position"] = Relationship(back_populates="asset")
