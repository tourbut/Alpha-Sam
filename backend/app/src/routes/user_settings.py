from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.core.db import get_session
from app.src.models.notification import NotificationSettings
from app.src.schemas.notification import NotificationSettingsRead, NotificationSettingsUpdate
from app.src.deps import get_current_user
from app.src.models.user import User

from app.src.crud import crud_notification

router = APIRouter()

@router.get("/me/settings", response_model=NotificationSettingsRead)
async def get_my_settings(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    현재 사용자의 알림 설정 조회.
    설정이 없으면 기본값으로 생성하여 반환합니다.
    """
    settings = await crud_notification.get_notification_settings(session, current_user.id)
    if not settings:
        settings = await crud_notification.create_default_notification_settings(session, current_user.id)
    return settings

@router.post("/me/settings", response_model=NotificationSettingsRead)
async def update_my_settings(
    settings_in: NotificationSettingsUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    현재 사용자의 알림 설정 업데이트 (Upsert).
    """
    return await crud_notification.update_notification_settings(
        session, current_user.id, settings_in
    )
