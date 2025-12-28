from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRead(schemas.BaseUser[int]):
    nickname: Optional[str] = None

class UserCreate(schemas.BaseUserCreate):
    nickname: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    nickname: Optional[str] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str
