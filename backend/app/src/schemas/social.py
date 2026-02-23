import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class LeaderboardEntry(BaseModel):
    user_id: uuid.UUID
    nickname: Optional[str] = None
    return_rate: float = Field(..., description="수익률 %")
    total_value: float = Field(..., description="총 평가금액")
    rank: int

class UserProfile(BaseModel):
    id: uuid.UUID
    nickname: Optional[str] = None
    email: str # 팔로잉 목록에서 이메일 보여줄지 여부는 기획에 따름. 일단 포함.

class FollowerResponse(BaseModel):
    id: uuid.UUID
    follower_id: uuid.UUID
    following_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class FollowListResponse(BaseModel):
    total: int
    users: List[UserProfile]
