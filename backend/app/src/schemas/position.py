import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from pydantic import field_validator
from decimal import Decimal


class PositionBase(SQLModel):
    asset_id: uuid.UUID
    quantity: float = Field(ge=0.0, description="보유 수량 (0 이상)")
    avg_price: float = Field(ge=0.0, description="평단가 (0 이상)")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        if v < 0:
            raise ValueError("quantity must be >= 0")
        return v

    @field_validator("avg_price")
    @classmethod
    def validate_avg_price(cls, v: float) -> float:
        if v < 0:
            raise ValueError("avg_price must be >= 0")
        return v


class PositionRead(PositionBase):
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # 계산된 필드
    valuation: Optional[float] = None
    profit_loss: Optional[float] = None
    return_rate: Optional[float] = None
    current_price: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class PositionWithAsset(PositionRead):
    """Asset 정보를 포함한 Position"""
    asset_symbol: Optional[str] = None
    asset_name: Optional[str] = None
    asset_category: Optional[str] = None


class AssetSummaryRead(SQLModel):
    """
    개별 자산 요약 정보 (프론트엔드 자산 상세 페이지용)
    """
    asset_id: uuid.UUID
    symbol: str
    name: str
    quantity: float
    avg_price: float  # 평균 매수가
    current_price: Optional[float] = None  # 현재가
    total_value: Optional[float] = None  # 평가금액
    profit_loss: Optional[float] = None  # 손익
    return_rate: Optional[float] = None  # 수익률 %
    
    model_config = ConfigDict(from_attributes=True)

