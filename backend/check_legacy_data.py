import asyncio
from sqlalchemy import select, func
from app.src.core.db import AsyncSessionLocal
from app.src.models.position import Position

async def main():
    async with AsyncSessionLocal() as session:
        # Check for positions without owner_id
        stmt = select(func.count()).where(Position.owner_id == None)
        result = await session.execute(stmt)
        count = result.scalar()
        
        print(f"Legacy Data Check Report")
        print(f"========================")
        if count > 0:
            print(f"[WARNING] Found {count} positions with missing owner_id (Legacy Data).")
        else:
            print(f"[OK] No legacy positions found (All have owner_id).")

if __name__ == "__main__":
    asyncio.run(main())
