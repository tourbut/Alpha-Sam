"""
Migration script to sync existing Positions to Transactions.
Creates a BUY transaction for each position that doesn't have one.
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.core.db import AsyncSessionLocal
from app.src.models.position import Position
from app.src.models.transaction import Transaction
from app.src.schemas.transaction import TransactionCreate
from app.src.crud import transactions as crud_transaction

async def migrate_positions():
    async with AsyncSessionLocal() as session:
        print("Starting migration: Positions -> Transactions")
        
        # 1. Fetch all positions
        stmt = select(Position)
        result = await session.execute(stmt)
        positions = result.scalars().all()
        
        migrated_count = 0
        skipped_count = 0
        
        for pos in positions:
            # Check if a transaction already exists for this asset and owner
            # (Simple check: if there are ANY transactions, we might skip or check if quantity matches)
            t_stmt = select(Transaction).where(
                Transaction.asset_id == pos.asset_id,
                Transaction.owner_id == pos.owner_id
            )
            t_result = await session.execute(t_stmt)
            existing_t = t_result.scalars().first()
            
            if existing_t:
                print(f"Skipping: Position {pos.id} (Asset {pos.asset_id}) already has transactions.")
                skipped_count += 1
                continue
            
            # Create a synthetic BUY transaction reflecting current state
            t_in = TransactionCreate(
                asset_id=pos.asset_id,
                type="BUY",
                quantity=pos.quantity,
                price=pos.buy_price
            )
            
            # We use a lower-level create to avoid triggering the Position update again 
            # or we can just create the Transaction record directly.
            # Actually, to be safe and consistent, let's just create the Transaction model.
            new_transaction = Transaction(
                asset_id=t_in.asset_id,
                owner_id=pos.owner_id,
                type=t_in.type,
                quantity=t_in.quantity,
                price=t_in.price,
                timestamp=pos.created_at # Use position creation time
            )
            session.add(new_transaction)
            migrated_count += 1
            print(f"Migrated: Created Transaction for Position {pos.id} (Asset {pos.asset_id})")
            
        await session.commit()
        print(f"Migration finished. Migrated: {migrated_count}, Skipped: {skipped_count}")

if __name__ == "__main__":
    asyncio.run(migrate_positions())
