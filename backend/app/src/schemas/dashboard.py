from typing import List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
from enum import Enum

class ActivityType(str, Enum):
    PORTFOLIO_CREATED = "portfolio_create"
    ASSET_ADDED = "asset_add"
    TRANSACTION_EXECUTED = "transaction"

class ActivityItem(BaseModel):
    id: uuid.UUID
    type: ActivityType
    title: str
    description: str
    timestamp: datetime
    entity_id: uuid.UUID
    portfolio_id: Optional[uuid.UUID] = None
    
    class Config:
        from_attributes = True
