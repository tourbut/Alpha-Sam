from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class TransactionBase(BaseModel):
    portfolio_id: int
    asset_id: int
    type: str # BUY, SELL
    quantity: float
    price: float
    executed_at: datetime

    @validator('type')
    def validate_type(cls, v):
        if v not in ('BUY', 'SELL'):
            raise ValueError('Type must be BUY or SELL')
        return v
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class TransactionCreate(BaseModel):
    asset_id: int # portfolio_id is taken from URL usually, but can be explicit
    type: str
    quantity: float
    price: float
    executed_at: Optional[datetime] = None # Defaults to now

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
