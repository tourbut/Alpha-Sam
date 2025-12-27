from pydantic import BaseModel, Field, computed_field, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class TransactionCreate(BaseModel):
    asset_id: int
    type: Literal["BUY", "SELL"]
    quantity: float = Field(gt=0, description="거래 수량")
    price: float = Field(gt=0, description="거래 단가")

class TransactionRead(BaseModel):
    id: int
    asset_id: int
    type: str
    quantity: float
    price: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.quantity * self.price

class TransactionList(BaseModel):
    items: list[TransactionRead]
    count: int
