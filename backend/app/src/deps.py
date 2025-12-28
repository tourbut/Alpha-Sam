from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.core.db import get_session
from app.src.models.user import User
from app.src.core.users import fastapi_users

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    user: Optional[User] = Depends(fastapi_users.current_user(active=True, optional=True))
) -> User:
    # 1. X-User-Id 헤더가 있으면 우선 사용 (개발 및 시뮬레이션 용도)
    if x_user_id:
        try:
            user_id = int(x_user_id)
            result = await session.execute(select(User).where(User.id == user_id))
            x_user = result.scalar_one_or_none()
            if x_user:
                if not x_user.is_active:
                    raise HTTPException(status_code=400, detail="Inactive user")
                return x_user
        except ValueError:
            pass # 숫자가 아니면 토큰 로직으로 폴백
            
    # 2. 기존 JWT 토큰 인증 로직 (fastapi-users)
    if user:
        return user
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
