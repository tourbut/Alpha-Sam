"""
알림 설정 모델
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, Boolean, ForeignKey

class NotificationSettings(SQLModel, table=True):
    """
    사용자별 알림 설정 모델
    """
    __tablename__ = "notification_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True),
        description="사용자 ID"
    )
    daily_report_enabled: bool = Field(default=True, description="일일 리포트 활성화 여부")
    price_alert_enabled: bool = Field(default=True, description="가격 알림 활성화 여부")
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
