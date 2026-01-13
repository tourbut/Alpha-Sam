from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func, String

if TYPE_CHECKING:
    from app.src.models.portfolio import Portfolio

class User(SQLModel, table=True):
    """
    사용자 모델
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String, unique=True, index=True) 
    )
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    nickname: Optional[str] = Field(default=None, max_length=50)
    is_public_leaderboard: bool = Field(default=False)
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    # Relationships
    portfolios: List["Portfolio"] = Relationship(back_populates="owner")
