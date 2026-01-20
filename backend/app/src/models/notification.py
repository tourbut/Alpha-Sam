"""
알림 설정 모델
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class NotificationSettings(SQLModel, table=True):
    """
    사용자별 알림 설정 모델
    """
    __tablename__ = "notification_settings"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True),
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
