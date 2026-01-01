"""
데이터베이스 연결 설정 모듈
SQLModel과 AsyncPG를 사용한 비동기 DB 엔진 구성
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_sam"
    environment: str = "dev"


settings = Settings()

# 비동기 엔진 생성
engine = create_async_engine(
    settings.database_url,
    echo=True,  # 개발 환경에서 SQL 쿼리 로그 출력
    future=True,
)

# 비동기 세션 팩토리 생성
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    의존성 주입을 위한 비동기 세션 생성기
    FastAPI의 Depends에서 사용
    """
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    데이터베이스 초기화 (테이블 생성)
    주의: 프로덕션에서는 Alembic 마이그레이션을 사용해야 함
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)



