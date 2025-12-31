from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.core import security
from app.src.core.db import get_session
from app.src.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False
)

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: Optional[str] = Depends(reusable_oauth2),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
) -> User:
    # 1. X-User-Id 헤더가 있으면 우선 사용 (개발 및 시뮬레이션 용도)
    if x_user_id:
        try:
            user_id = int(x_user_id)
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                if not user.is_active:
                    raise HTTPException(status_code=400, detail="Inactive user")
                return user
        except ValueError:
            pass # 숫자가 아니면 토큰 로직으로 폴백
            
    # 2. 기존 JWT 토큰 인증 로직
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM], options={"verify_aud": False}
        )
        token_user_id: str = payload.get("sub")
        if token_user_id is None:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        
    result = await session.execute(select(User).where(User.id == int(token_user_id)))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user
