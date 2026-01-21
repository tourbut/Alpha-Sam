import uuid
from sqlmodel import SQLModel, Field
from pydantic import computed_field, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class TransactionCreate(SQLModel):
    portfolio_id: uuid.UUID
    asset_id: uuid.UUID
    type: Literal["BUY", "SELL"]
    quantity: float = Field(gt=0, description="거래 수량")
    price: float = Field(gt=0, description="거래 단가")
    executed_at: Optional[datetime] = Field(None, description="거래 실행 일시")

class TransactionRead(SQLModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    type: str
    quantity: float
    price: float
    executed_at: datetime  # timestamp → executed_at으로 변경
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.quantity * self.price

class TransactionList(SQLModel):
    items: list[TransactionRead]
    count: int


class TransactionWithDetails(SQLModel):
    """
    거래 내역 상세 정보 (프론트엔드 자산 상세 페이지용)
    """
    id: uuid.UUID
    type: str  # "buy" 또는 "sell" (소문자 변환)
    date: datetime  # executed_at
    quantity: float
    price: float
    total: float  # quantity * price
    fee: Optional[float] = None  # 수수료 (현재 모델에 없음, 향후 확장용)
    
    model_config = ConfigDict(from_attributes=True)
