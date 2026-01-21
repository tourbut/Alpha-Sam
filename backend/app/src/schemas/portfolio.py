from typing import List, Optional, Literal
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from app.src.schemas.position import PositionWithAsset
from app.src.models.portfolio import PortfolioVisibility

class PortfolioBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    currency: str = Field(default="USD")

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioRead(PortfolioBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    visibility: PortfolioVisibility
    share_token: Optional[uuid.UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class PortfolioVisibilityUpdate(SQLModel):
    visibility: PortfolioVisibility

# 공유된 포트폴리오 조회용
class PortfolioSharedRead(SQLModel):
    id: uuid.UUID
    name: str
    owner_nickname: Optional[str] = None # 닉네임 추가 예정
    description: Optional[str] = None
    total_value: Optional[float] = None
    return_rate: Optional[float] = None
    positions: List[PositionWithAsset] = []
    visibility: PortfolioVisibility

class PortfolioStats(SQLModel):
    percent: Optional[float] = Field(None, description="수익률 (%)")
    direction: Literal["up", "down", "flat"] = Field("flat", description="수익 방향")

class PortfolioSummary(SQLModel):
    total_value: Optional[float] = Field(None, description="총 평가금액")
    total_cost: Optional[float] = Field(None, description="총 매수금액")
    total_pl: Optional[float] = Field(None, description="총 손익금액")
    total_pl_stats: PortfolioStats = Field(default_factory=PortfolioStats, description="손익 통계")

class PortfolioResponse(SQLModel):
    summary: PortfolioSummary
    positions: List[PositionWithAsset]

class PortfolioHistoryRead(SQLModel):
    id: uuid.UUID
    total_value: float
    total_cost: float
    total_pl: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 포트폴리오 목록 + 자산 요약 조회용 스키마
class PortfolioAssetSummary(SQLModel):
    """개별 자산 요약 정보"""
    symbol: str = Field(description="자산 심볼 (예: BTC, ETH)")
    name: str = Field(description="자산 이름 (예: Bitcoin)")
    value: float = Field(description="해당 자산의 현재 평가금액")
    percentage: float = Field(description="포트폴리오 내 비중 (%)")

class PortfolioWithAssetsSummary(SQLModel):
    """포트폴리오 + 자산 요약 정보 (목록 조회용)"""
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    total_value: float = Field(default=0.0, description="총 평가금액")
    assets: List[PortfolioAssetSummary] = Field(default_factory=list, description="자산 구성 리스트")
    
    model_config = ConfigDict(from_attributes=True)
