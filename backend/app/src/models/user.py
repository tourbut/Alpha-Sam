from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, String, Boolean
from fastapi_users.db import SQLAlchemyBaseUserTable

class User(SQLAlchemyBaseUserTable[int], SQLModel, table=True):
    """
    사용자 모델
    """
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False) 
    )
    hashed_password: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True, sa_column=Column(Boolean, default=True, nullable=False))
    is_superuser: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))
    is_verified: bool = Field(default=True, sa_column=Column(Boolean, default=True, nullable=False))
    nickname: Optional[str] = Field(default=None, max_length=50)
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
