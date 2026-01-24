from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core import security
from app.src.models.user import User
from app.src.schemas.user import UserCreate, UserRead, Token
from app.src.crud import users as crud_user
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(
    user_in: UserCreate,
    session: SessionDep_async
) -> Any:
    """
    Create new user without the need to be logged in
    """
    user = await crud_user.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
        
    user = await crud_user.create_user(session=session, obj_in=user_in)
    return user

@router.post("/login", response_model=Token)
async def login(
    session: SessionDep_async,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    access_token = security.create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: CurrentUser,
) -> Any:
    """
    Get current user
    """
    return current_user
