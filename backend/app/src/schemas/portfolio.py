from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.src.schemas.position import PositionWithAsset

class PortfolioStats(BaseModel):
    percent: Optional[float] = Field(None, description="수익률 (%)")
    direction: Literal["up", "down", "flat"] = Field("flat", description="수익 방향")

class PortfolioSummary(BaseModel):
    total_value: Optional[float] = Field(None, description="총 평가금액")
    total_cost: Optional[float] = Field(None, description="총 매수금액")
    total_pl: Optional[float] = Field(None, description="총 손익금액")
    total_pl_stats: PortfolioStats = Field(default_factory=PortfolioStats, description="손익 통계")

class PortfolioResponse(BaseModel):
    summary: PortfolioSummary
    positions: List[PositionWithAsset]

class PortfolioHistoryRead(BaseModel):
    id: int
    total_value: float
    total_cost: float
    total_pl: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
