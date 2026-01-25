import asyncio
import os
import sys

# Add backend path to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.src.core.db import AsyncSessionLocal
from app.src.models.admin import AdminAsset
from app.src.services.price_collector import price_collector
from app.src.core.cache import cache_service
from app.src.core.config import settings

async def qa_verify_workflow():
    print("--- 1. Setup: Creating Admin Asset (NVDA) ---")
    async with AsyncSessionLocal() as session:
        # Check if exists
        from sqlalchemy import select
        stmt = select(AdminAsset).where(AdminAsset.symbol == "NVDA")
        existing = (await session.execute(stmt)).scalar_one_or_none()
        
        if not existing:
            asset = AdminAsset(symbol="NVDA", name="NVIDIA Corp", type="STOCK", is_active=True)
            session.add(asset)
            await session.commit()
            print(">> Created AdminAsset: NVDA")
        else:
            print(">> AdminAsset NVDA already exists")

    print("\n--- 2. Execution: Running PriceCollector Service ---")
    async with AsyncSessionLocal() as session:
        # Simulate Celery Task Logic
        results = await price_collector.collect_active_assets(session)
        print(f">> Collection Results: {results}")

    print("\n--- 3. Verification: Checking Redis Cache ---")
    redis_value = await cache_service.get("price:NVDA")
    print(f">> Redis 'price:NVDA': {redis_value}")
    
    if redis_value and float(redis_value) > 0:
        print("\n>>> QA PASS: Price successfully collected and cached.")
    else:
        print("\n>>> QA FAIL: Price not found in Redis.")

if __name__ == "__main__":
    # Ensure env vars are loaded similar to app
    asyncio.run(qa_verify_workflow())
