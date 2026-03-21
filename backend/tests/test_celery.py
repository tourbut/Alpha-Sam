
import sys
import os
import asyncio
import redis
import json
import time

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.src.services.tasks.price_tasks import collect_market_prices
from app.celery_app import celery_app

def test_celery_task():
    print("🚀 Triggering Celery Task: collect_market_prices...")
    
    # 1. Trigger the task asynchronously
    # We use send_task or .delay() depending on import availability.
    # Since we imported the function which is decorated, .delay() works.
    task = collect_market_prices.delay()
    print(f"✅ Task Sent! Task ID: {task.id}")
    
    print("⏳ Waiting for task to complete (10 seconds)...")
    time.sleep(10)
    
    # 2. Check Redis for results
    # Default Redis URL from settings
    redis_url = "redis://localhost:6379/0"
    r = redis.from_url(redis_url)
    
    print("\n🔍 Checking Redis for 'price:AAPL'...")
    price_data = r.get("price:AAPL")
    
    if price_data:
        print(f"✅ Found price data for AAPL: {price_data.decode('utf-8')}")
    else:
        print("⚠️ 'price:AAPL' not found in Redis. Task might have failed or no active asset 'AAPL' exists.")
        
    # Check Celery Result if possible (requires result backend)
    # result = task.result # This blocks if we want, but we waited 10s.
    if task.ready():
        print(f"✅ Task State: {task.state}")
        print(f"✅ Task Result: {task.result}")
    else:
        print(f"ℹ️ Task State: {task.state} (Still pending or processing)")

if __name__ == "__main__":
    test_celery_task()
