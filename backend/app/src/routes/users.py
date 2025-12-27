from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.db import get_session
from app.src.core import security
from app.src import deps
from app.src.models.user import User
from app.src.schemas.user import UserRead, UserUpdate, UserPasswordUpdate
from app.src.crud import crud_user

router = APIRouter()

@router.put("/me", response_model=UserRead)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update own user (nickname, etc)
    """
    user = await crud_user.update_user(session, db_user=current_user, obj_in=user_in)
    return user

@router.post("/password", status_code=status.HTTP_200_OK)
async def update_password(
    password_in: UserPasswordUpdate,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update own password
    """
    if not security.verify_password(password_in.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    if password_in.current_password == password_in.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as current password")

    hashed_password = security.get_password_hash(password_in.new_password)
    await crud_user.update_user_password(session, db_user=current_user, password=hashed_password)
    
    return {"message": "Password updated successfully"}
