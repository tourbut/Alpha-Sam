from sqlmodel import SQLModel, Field
from pydantic import computed_field, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class TransactionCreate(SQLModel):
    portfolio_id: int
    asset_id: int
    type: Literal["BUY", "SELL"]
    quantity: float = Field(gt=0, description="거래 수량")
    price: float = Field(gt=0, description="거래 단가")
    executed_at: Optional[datetime] = Field(None, description="거래 실행 일시")

class TransactionRead(SQLModel):
    id: int
    asset_id: int
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
