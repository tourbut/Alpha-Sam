from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class AdminAssetBase(BaseModel):
    symbol: str
    name: str
    type: str
    currency: str = "USD"
    is_active: bool = True

class AdminAssetCreate(AdminAssetBase):
    pass

class AdminAssetRead(AdminAssetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
