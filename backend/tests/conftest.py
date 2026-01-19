import pytest
import random
import string
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.src.core.db import settings

import pytest_asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import all models to ensure metadata is populated
from app.src.models import *

@pytest_asyncio.fixture
async def test_session():
    # Use In-Memory SQLite for independent testing
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        DATABASE_URL, 
        echo=False, 
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()

@pytest.fixture
def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com"

@pytest.fixture
def random_nickname():
    return f"nick_{''.join(random.choices(string.ascii_lowercase, k=8))}"
