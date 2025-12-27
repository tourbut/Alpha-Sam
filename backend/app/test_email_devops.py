from app.src.engine.tasks.email_tasks import send_price_alert
import time

def test_email_alert():
    print("Trigging test price alert email via Celery...")
    send_price_alert.delay(
        to_email="test@example.com",
        symbol="AAPL",
        price=150.0,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    print("Task triggered. Check celery-worker logs and MailHog at http://localhost:8025")

if __name__ == "__main__":
    test_email_alert()
