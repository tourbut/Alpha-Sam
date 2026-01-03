from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core import security
from app.src.models.user import User
from app.src.schemas.user import UserRead, UserUpdate, UserPasswordUpdate
from app.src.crud import crud_user
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter()

@router.put("/me", response_model=UserRead)
async def update_user_me(
    user_in: UserUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    Update own user (nickname, etc)
    """
    user = await crud_user.update_user(session=session, db_user=current_user, obj_in=user_in)
    return user

@router.post("/password", status_code=status.HTTP_200_OK)
async def update_password(
    password_in: UserPasswordUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    Update own password
    """
    if not security.verify_password(password_in.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    if password_in.current_password == password_in.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as current password")

    hashed_password = security.get_password_hash(password_in.new_password)
    await crud_user.update_user_password(session=session, db_user=current_user, password=hashed_password)
    
    return {"message": "Password updated successfully"}
