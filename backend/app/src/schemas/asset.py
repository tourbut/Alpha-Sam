import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class AssetBase(SQLModel):
    symbol: str = Field(..., description="자산 심볼 (예: AAPL, BTC)")
    name: str = Field(..., description="자산 이름")
    category: Optional[str] = Field(None, description="자산 카테고리 (예: EQUITY, CRYPTO)")

class AssetCreate(SQLModel):
    portfolio_id: uuid.UUID = Field(..., description="귀속 포트폴리오 ID")
    symbol: str = Field(..., description="자산 심볼")
    name: Optional[str] = Field(None, description="자산 이름 (미입력 시 자동 검색 시도)")
    category: Optional[str] = Field(None, description="자산 카테고리")
    owner_id: Optional[uuid.UUID] = Field(None, description="소유자 ID (내부용)")

class AssetRead(AssetBase):
    id: uuid.UUID = Field(..., description="자산 ID")
    portfolio_id: uuid.UUID = Field(..., description="귀속 포트폴리오 ID")
    owner_id: Optional[uuid.UUID] = Field(None, description="소유자 ID")
    created_at: datetime = Field(..., description="생성 일시")
    updated_at: datetime = Field(..., description="수정 일시")
    latest_price: Optional[float] = Field(None, description="최신 현재가")
    latest_price_updated_at: Optional[datetime] = Field(None, description="현재가 업데이트 시간")
    # Position 정보 (계산된 필드)
    quantity: Optional[float] = Field(None, description="보유 수량")
    avg_price: Optional[float] = Field(None, description="평균 매수 단가")
    buy_price: Optional[float] = Field(None, description="평균 매수 단가 (avg_price 별칭)")
    valuation: Optional[float] = Field(None, description="평가 금액")
    profit_loss: Optional[float] = Field(None, description="손익 금액")
    return_rate: Optional[float] = Field(None, description="수익률 (%)")

    model_config = ConfigDict(from_attributes=True)
