import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.models.notification import NotificationSettings
from app.src.schemas.notification import NotificationSettingsUpdate

async def get_notification_settings(*, session: AsyncSession, user_id: uuid.UUID) -> Optional[NotificationSettings]:
    """
    사용자의 알림 설정 조회. 없으면 생성하지 않고 None 반환 (API 레벨에서 처리 권장)
    """
    try:
        stmt = select(NotificationSettings).where(NotificationSettings.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        print(e)
        raise e

async def create_default_notification_settings(*, session: AsyncSession, user_id: uuid.UUID) -> NotificationSettings:
    """
    기본 알림 설정 생성
    """
    try:
        settings = NotificationSettings(user_id=user_id)
        session.add(settings)
        await session.commit()
        await session.refresh(settings)
        return settings
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

async def update_notification_settings(
    *,
    session: AsyncSession, 
    user_id: uuid.UUID, 
    settings_in: NotificationSettingsUpdate
) -> NotificationSettings:
    """
    알림 설정 업데이트 (없으면 생성 - Upsert)
    """
    try:
        settings = await get_notification_settings(session=session, user_id=user_id)
        if not settings:
            settings = NotificationSettings(user_id=user_id, **settings_in.model_dump())
            session.add(settings)
        else:
            obj_data = settings_in.model_dump(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(settings, key, value)
            session.add(settings)
            
        await session.commit()
        await session.refresh(settings)
        return settings
    except Exception as e:
        print(e)
        await session.rollback()
        raise e
