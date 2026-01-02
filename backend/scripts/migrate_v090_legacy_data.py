import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from app.src.core.db import AsyncSessionLocal
from app.src.models.position import Position

async def migrate():
    print("🚀 Starting Migration: Legacy Data Cleanup (v0.9.0)")
    
    async with AsyncSessionLocal() as session:
        # 1. Check for positions with NULL owner_id
        count_stmt = select(func.count()).select_from(Position).where(Position.owner_id == None)
        result = await session.execute(count_stmt)
        count = result.scalar()
        
        print(f"📊 Found {count} positions with NULL owner_id.")
        
        if count == 0:
            print("✅ No legacy data found. Migration skipped.")
            return

        # 2. Update owner_id to 1 (Default Admin)
        # Using a select and loop for update to ensure we can count accurately if needed, 
        # or use update statement directly. direct update is better for perf.
        # But we need to make sure '1' exists? Assuming ID 1 is safe as per plan.
        
        from sqlalchemy import update
        update_stmt = (
            update(Position)
            .where(Position.owner_id == None)
            .values(owner_id=1)
        )
        
        await session.execute(update_stmt)
        await session.commit()
        
        print(f"✅ Successfully updated {count} rows. All legacy positions now belong to User ID 1.")

if __name__ == "__main__":
    asyncio.run(migrate())
