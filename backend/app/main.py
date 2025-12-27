from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from sqlalchemy import text

from app.src.core.db import engine, init_db
from app.src.core.cache import close_redis_client
from app.src.models import Asset, Price, Position

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작/종료 시 실행되는 lifespan 이벤트
    - 시작 시: DB 연결 테스트 및 초기화
    - 종료 시: 리소스 정리
    """
    # 시작 시
    logger.info("애플리케이션 시작 중...")
    
    try:
        # DB 연결 테스트
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info(f"데이터베이스 연결 성공: {result.scalar()}")
        
        # 테이블 초기화 (개발 환경용, 프로덕션에서는 Alembic 사용)
        # await init_db()
        logger.info("데이터베이스 초기화 완료")
        
    except Exception as e:
        logger.error(f"데이터베이스 연결 실패: {e}")
        raise
    
    yield
    
    # 종료 시
    logger.info("애플리케이션 종료 중...")
    await engine.dispose()
    await close_redis_client()
    logger.info("데이터베이스 및 Redis 연결 종료 완료")


app = FastAPI(
    title="Alpha-Sam API",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to Alpha-Sam API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

from app.src.api import api_router
from app.src.routes.market import router as market_router

app.include_router(api_router, prefix="/api/v1")
app.include_router(market_router, prefix="/api/v1/market", tags=["Market Data"])
