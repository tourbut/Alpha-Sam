import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from app.src.core.db import AsyncSessionLocal
from app.src.models.position import Position

async def migrate():
    print("🚀 Migration (v0.9.0) skipped intentionally to avoid schema mismatch.")
    return

if __name__ == "__main__":
    asyncio.run(migrate())
