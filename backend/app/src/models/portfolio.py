"""
Portfolio (포트폴리오) 모델
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, String, func

# Circular import avoidance
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.src.models.user import User
    from app.src.models.transaction import Transaction

class Portfolio(SQLModel, table=True):
    """
    포트폴리오 모델
    
    Attributes:
        id: ID
        owner_id: 소유자 User ID
        name: 포트폴리오 이름
        description: 설명
        currency: 기준 통화 (USD, KRW 등)
        created_at: 생성 시각
    """
    __tablename__ = "portfolios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="소유자 User ID"
    )
    name: str = Field(
        sa_column=Column(String(100), nullable=False),
        description="포트폴리오 이름"
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255)),
        description="포트폴리오 설명"
    )
    currency: str = Field(
        default="USD",
        sa_column=Column(String(10)),
        description="기준 통화"
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
    owner: "User" = Relationship(back_populates="portfolios")
    transactions: List["Transaction"] = Relationship(back_populates="portfolio")
