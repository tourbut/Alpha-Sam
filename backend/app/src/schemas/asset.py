from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AssetBase(BaseModel):
    symbol: str
    name: str
    category: Optional[str] = None

class AssetCreate(BaseModel):
    symbol: str
    name: Optional[str] = None
    category: Optional[str] = None
    owner_id: Optional[int] = None

class AssetRead(AssetBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    latest_price: Optional[float] = None
    latest_price_updated_at: Optional[datetime] = None
    # Position 정보 (계산된 필드)
    quantity: Optional[float] = None
    buy_price: Optional[float] = None
    valuation: Optional[float] = None
    profit_loss: Optional[float] = None
    return_rate: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
