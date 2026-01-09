from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

class PortfolioShareBase(BaseModel):
    settings: Dict = Field(default_factory=dict)
    is_active: bool = True

class PortfolioShareCreate(PortfolioShareBase):
    pass

class PortfolioShareRead(PortfolioShareBase):
    id: UUID
    user_id: int
    created_at: datetime
    expired_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    user_id: int
    nickname: Optional[str] = None
    pnl_percent: float
    rank: int
