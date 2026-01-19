"""
Redis 캐싱 설정 모듈
"""
import json
from typing import Optional
import redis.asyncio as redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class CacheSettings(BaseSettings):
    """캐시 설정"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    redis_url: str = "redis://localhost:6379/0"


cache_settings = CacheSettings()

# Redis 클라이언트 (전역)
_redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """
    Redis 클라이언트 싱글톤 반환
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            cache_settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_client


async def close_redis_client() -> None:
    """
    Redis 클라이언트 연결 종료
    """
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


class CacheService:
    """
    Redis 캐싱 서비스
    """
    
    def __init__(self, ttl: int = 300):
        """
        Args:
            ttl: 캐시 TTL (초 단위, 기본값 5분)
        """
        self.ttl = ttl
    
    async def get(self, key: str) -> Optional[str]:
        """
        캐시에서 값 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            캐시된 값 또는 None
        """
        client = await get_redis_client()
        try:
            return await client.get(key)
        except Exception as e:
            # Redis 연결 실패 시 None 반환 (캐시 미스로 처리)
            print(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """
        캐시에 값 저장
        
        Args:
            key: 캐시 키
            value: 저장할 값
            ttl: TTL (초 단위, None이면 기본값 사용)
        
        Returns:
            성공 여부
        """
        client = await get_redis_client()
        try:
            ttl = ttl or self.ttl
            await client.setex(key, ttl, value)
            return True
        except Exception as e:
            # Redis 연결 실패 시 False 반환 (캐시 실패로 처리)
            print(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        캐시에서 값 삭제
        
        Args:
            key: 캐시 키
        
        Returns:
            성공 여부
        """
        client = await get_redis_client()
        try:
            await client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """
        패턴에 맞는 모든 키 삭제
        
        Args:
            pattern: 키 패턴 (예: "price:*")
        
        Returns:
            삭제된 키 개수
        """
        client = await get_redis_client()
        try:
            keys = []
            async for key in client.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                return await client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Redis delete_pattern error: {e}")
            return 0


# 전역 캐시 서비스 인스턴스
cache_service = CacheService(ttl=300)  # 5분 TTL

