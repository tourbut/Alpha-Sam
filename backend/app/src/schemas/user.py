from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

class Token(BaseModel):
    access_token: str
    token_type: str

# Shared properties
class UserBase(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    nickname: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: str
    password: str

# Properties to receive via API on update
class UserUpdate(SQLModel):
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None

class UserPasswordUpdate(SQLModel):
    current_password: str
    new_password: str

# Properties to return to client
class UserRead(SQLModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    nickname: Optional[str] = None
