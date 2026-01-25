import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class AdminAsset(SQLModel, table=True):
    __tablename__ = "admin_assets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(index=True, unique=True)
    name: str
    type: str  # STOCK, CRYPTO, FOREX, INDEX
    currency: str = Field(default="USD")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
