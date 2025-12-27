import os
import sys
from datetime import datetime

# backend 디렉토리를 path에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.src.engine.tasks.email_tasks import send_price_alert, send_daily_report_email
from app.src.core.email_service import email_settings

def check_settings():
    print("--- Checking Email Settings ---")
    print(f"EMAILS_ENABLED: {email_settings.EMAILS_ENABLED}")
    print(f"SMTP_HOST: {email_settings.SMTP_HOST}")
    print(f"SMTP_PORT: {email_settings.SMTP_PORT}")
    if not email_settings.EMAILS_ENABLED:
        print("[!] Warning: EMAILS_ENABLED is False. Emails will be MOCKED (logged only).")
        print("To enable real sending (to MailHog), set EMAILS_ENABLED=True in backend/.env")
    print("-" * 30)

def test_price_alert():
    print("\n--- Testing Price Alert Task ---")
    to_email = "test@example.com"
    symbol = "AAPL"
    price = 150.0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Queueing price alert for {symbol} to {to_email}...")
    result = send_price_alert.delay(to_email, symbol, price, timestamp)
    print(f"Task sent. ID: {result.id}")
    return result

def test_daily_report():
    print("\n--- Testing Daily Report Task ---")
    to_email = "test@example.com"
    user_nickname = "AlphaTester"
    report_data = {
        "date_str": datetime.now().strftime("%Y-%m-%d"),
        "total_valuation": 10000.0,
        "total_profit_loss": 500.0,
        "return_rate": 5.0
    }
    
    print(f"Queueing daily report to {to_email}...")
    result = send_daily_report_email.delay(to_email, user_nickname, report_data)
    print(f"Task sent. ID: {result.id}")
    return result

if __name__ == "__main__":
    print("=" * 40)
    print("Alpha-Sam Manual Email Trigger Test")
    print("=" * 40)
    
    check_settings()
    
    alert_res = test_price_alert()
    report_res = test_daily_report()
    
    print("\n" + "=" * 40)
    print("SUCCESS: Tasks have been queued to Celery.")
    print("-" * 40)
    print("1. Check Celery Worker logs for execution details.")
    print("2. Check MailHog UI to see the actual emails:")
    print("   URL: http://localhost:8025")
    print("=" * 40)
