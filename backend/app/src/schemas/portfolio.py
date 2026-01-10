from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    currency: str = "USD"

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioRead(PortfolioBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
