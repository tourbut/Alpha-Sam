"""
Asset (자산) 모델
사용자가 관리하는 개별 투자 대상을 나타냄
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, DateTime, func


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
    
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id", description="Owner User ID")
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
    prices: list["Price"] = Relationship(back_populates="asset")
    transactions: list["Transaction"] = Relationship(back_populates="asset")


