"""
Celery 앱 초기화
Redis를 브로커로 사용하여 비동기 작업 처리
"""
from celery import Celery
from celery.schedules import crontab
from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    """Celery 설정"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"


celery_settings = CelerySettings()

# Celery 앱 생성
celery_app = Celery(
    "alpha_sam",
    broker=celery_settings.celery_broker_url,
    backend=celery_settings.celery_result_backend,
    include=[
        "app.src.services.tasks.price_tasks", 
        "app.src.services.tasks.email_tasks",
        "app.src.services.tasks.report_tasks"
    ],  # 태스크 모듈 포함
)

# Celery 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30분
    task_soft_time_limit=25 * 60,  # 25분
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=600,  # 결과 만료 시간 10분 (600초)
    # Celery Beat 스케줄 설정
    beat_schedule={
        "collect-market-prices": {
            "task": "app.src.services.tasks.price_tasks.collect_market_prices",
            "schedule": 60.0,  # 1분마다 실행 (시스템 자산 수집)
        },
        "update-all-prices": {
            "task": "app.src.services.tasks.price_tasks.update_all_prices",
            "schedule": 300.0,  # 5분마다 실행 (기존 로직 유지)
        },
        "daily-portfolio-report": {
            "task": "app.src.services.tasks.report_tasks.daily_portfolio_report_job",
            "schedule": crontab(hour=0, minute=0),  # Daily at 00:00 UTC (09:00 KST)
        },
    },
)

