import logging
import redis
from app.celery_app import celery_app, celery_settings
from app.src.core.email_service import email_service
from app.src.core.logging_utils import mask_email

logger = logging.getLogger(__name__)

# Sync Redis client for blocking tasks
redis_client = redis.from_url(celery_settings.redis_url, decode_responses=True)

@celery_app.task(
    name="app.src.engine.tasks.email_tasks.send_price_alert",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5
)
def send_price_alert(to_email: str, symbol: str, price: float, timestamp: str):
    """
    Send price alert email task with rate limiting (1 per 24h per asset).
    """
    lock_key = f"email_lock:{to_email}:price_alert:{symbol}"
    
    # Check if already sent in the last 24h
    if redis_client.get(lock_key):
        logger.info(f"Rate Limit: Price alert for {symbol} already sent to {mask_email(to_email)} recently.")
        return {"status": "skipped", "reason": "rate_limit"}

    logger.info(f"Task: Sending price alert for {symbol} to {mask_email(to_email)}")
    context = {
        "symbol": symbol,
        "price": price,
        "timestamp": timestamp
    }
    try:
        email_service.send_email(
            to_email=to_email, 
            subject=f"Price Alert: {symbol}", 
            template_name="alert.html", 
            context=context
        )
        # Set lock for 24 hours
        redis_client.setex(lock_key, 86400, "1")
        return {"status": "success", "to": to_email}
    except Exception as e:
        logger.error(f"Error in send_price_alert task: {e}")
        raise e  # Re-raise to trigger Celery retry

@celery_app.task(
    name="app.src.engine.tasks.email_tasks.send_daily_report_email",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5
)
def send_daily_report_email(to_email: str, user_nickname: str, report_data: dict):
    """
    Send daily portfolio report email task with rate limiting (1 per day).
    """
    date_str = report_data.get("date_str")
    lock_key = f"email_lock:{to_email}:daily_report:{date_str}"
    
    if redis_client.get(lock_key):
        logger.info(f"Rate Limit: Daily report for {date_str} already sent to {mask_email(to_email)}.")
        return {"status": "skipped", "reason": "rate_limit"}

    logger.info(f"Task: Sending daily report to {mask_email(to_email)}")
    
    is_positive = report_data.get("total_profit_loss", 0) >= 0
    context = {
        "user_nickname": user_nickname or "Invester",
        "date_str": date_str,
        "total_valuation": report_data.get("total_valuation", 0),
        "total_profit_loss": report_data.get("total_profit_loss", 0),
        "return_rate": report_data.get("return_rate", 0),
        "is_positive": is_positive
    }
    
    try:
        email_service.send_email(
            to_email=to_email,
            subject=f"Daily Portfolio Report - {date_str}",
            template_name="daily_report.html",
            context=context
        )
        # Lock for 24 hours
        redis_client.setex(lock_key, 86400, "1")
        return {"status": "success", "to": to_email}
    except Exception as e:
        logger.error(f"Error in send_daily_report_email task: {e}")
        raise e  # Re-raise to trigger Celery retry
