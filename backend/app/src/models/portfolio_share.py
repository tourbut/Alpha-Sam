from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, JSON

class PortfolioShare(SQLModel, table=True):
    """
    포트폴리오 공유 모델
    """
    __tablename__ = "portfolio_shares"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # 공유 설정 (예: {"show_amounts": false, "show_pnl": true})
    settings: dict = Field(default_factory=dict, sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    # Optional: 만료일 설정 가능
    expired_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True))
    )
