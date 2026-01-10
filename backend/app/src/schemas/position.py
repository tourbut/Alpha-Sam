"""
Position (보유 내역) 스키마
"""
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from pydantic import field_validator
from decimal import Decimal


class PositionBase(SQLModel):
    asset_id: int
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


class PositionCreate(PositionBase):
    pass


class PositionUpdate(SQLModel):
    quantity: Optional[float] = Field(default=None, ge=0.0)
    avg_price: Optional[float] = Field(default=None, ge=0.0)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("quantity must be >= 0")
        return v

    @field_validator("avg_price")
    @classmethod
    def validate_avg_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("avg_price must be >= 0")
        return v


class PositionRead(PositionBase):
    id: int
    created_at: datetime
    updated_at: datetime
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

