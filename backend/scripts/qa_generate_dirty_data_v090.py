import asyncio
import sys
import os

# Add backend directory to sys.path to allow imports from app
# Assuming this script is in backend/scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.src.core.db import AsyncSessionLocal
from app.src.models.asset import Asset

async def main():
    print("Generating dirty data for v0.9.0 migration testing...")
    
    async with AsyncSessionLocal() as session:
        # Scenario 1: Legacy Position without Owner
        # We use raw SQL to bypass SQLAlchemy/Pydantic validation if owner_id is required in model
        from sqlalchemy import text
        
        # 1. Ensure an asset exists to link to
        asset_stmt = text("INSERT INTO assets (symbol, name, category, created_at, updated_at) VALUES ('LEGACY_POS_ASSET', 'Legacy Coin', 'Test', NOW(), NOW()) RETURNING id")
        try:
            result = await session.execute(asset_stmt)
            asset_id = result.scalar()
            print(f"✅ Created Asset for legacy position: ID={asset_id}")
            
            # 2. Insert Position with owner_id = NULL
            pos_stmt = text("""
                INSERT INTO positions (asset_id, owner_id, quantity, buy_price, buy_date, created_at, updated_at)
                VALUES (:asset_id, NULL, 100, 50.0, NOW(), NOW(), NOW())
                RETURNING id
            """)
            
            pos_result = await session.execute(pos_stmt, {"asset_id": asset_id})
            pos_id = pos_result.scalar()
            
            await session.commit()
            print(f"✅ [SUCCESS] Created Dirty Position: ID={pos_id} with owner_id=NULL")
            
        except Exception as e:
            print(f"❌ [ERROR] Failed to create dirty data: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(main())
