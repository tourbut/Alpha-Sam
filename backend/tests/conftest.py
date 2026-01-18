import pytest
import random
import string
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.src.core.db import settings

@pytest.fixture
async def test_session():
    # Use database_url from settings
    engine = create_async_engine(str(settings.database_url), echo=False, future=True)
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
