
import asyncio
import logging
from datetime import datetime
from sqlalchemy import select, desc
from app.celery_app import celery_app
from app.src.core.db import AsyncSessionLocal
from app.src.models.user import User
from app.src.models.prices_day import PriceDay
from app.src.services.portfolio_calculator import calculate_portfolio_summary
from app.src.services.tasks.email_tasks import send_daily_report_email

from app.src.models.notification import NotificationSettings

logger = logging.getLogger(__name__)

async def _process_daily_reports():
    async with AsyncSessionLocal() as session:
        # 1. 활성 사용자 조회
        result = await session.execute(select(User).where(User.is_active == True))
        users = result.scalars().all()
        
        logger.info(f"Starting daily report job for {len(users)} users.")
        
        today_str = datetime.now().strftime("%Y-%m-%d")

        for user in users:
            try:
                # 1.5 알림 설정 확인
                settings_stmt = select(NotificationSettings).where(NotificationSettings.user_id == user.id)
                settings_result = await session.execute(settings_stmt)
                settings = settings_result.scalar_one_or_none()
                
                # 설정이 없으면 기본적으로 True로 간주하거나, 조용히 건너뜁니다.
                # 여기서는 명시적으로 꺼져 있는 경우에만 건너뜁니다.
                if settings and not settings.daily_report_enabled:
                    logger.info(f"Skipping daily report for user {user.id} (disabled in settings)")
                    continue

                from app.src.services.portfolio_service import PortfolioService
                portfolio_response = await PortfolioService.get_summary(session, user_id=user.id)
                
                if not portfolio_response or not portfolio_response.positions:
                    continue
                
                metrics = portfolio_response.summary
                
                report_data = {
                    "date_str": today_str,
                    "total_valuation": round(metrics.total_value, 2),
                    "total_profit_loss": round(metrics.total_pl, 2),
                    "return_rate": metrics.total_pl_stats.percent
                }
                
                # 5. 이메일 태스크 발행
                send_daily_report_email.delay(
                    to_email=user.email,
                    user_nickname=user.nickname,
                    report_data=report_data
                )
                
            except Exception as e:
                logger.error(f"Error processing report for user {user.id}: {e}")

@celery_app.task(name="app.src.services.tasks.report_tasks.daily_portfolio_report_job")
def daily_portfolio_report_job():
    """
    매일 실행되는 포트폴리오 리포트 발송 배치 작업
    """
    logger.info("Daily portfolio report job started.")
    try:
        asyncio.run(_process_daily_reports())
    except Exception as e:
        logger.error(f"Daily report job failed: {e}")
