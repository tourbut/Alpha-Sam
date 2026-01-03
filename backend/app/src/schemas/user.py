from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel
from fastapi_users import schemas

class Token(SQLModel):
    access_token: str
    token_type: str

# Shared properties
class UserBase(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    nickname: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(schemas.BaseUserCreate):
    nickname: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(schemas.BaseUserUpdate):
    nickname: Optional[str] = None

class UserPasswordUpdate(SQLModel):
    current_password: str
    new_password: str

# Properties to return to client
class UserRead(schemas.BaseUser[int]):
    nickname: Optional[str] = None
