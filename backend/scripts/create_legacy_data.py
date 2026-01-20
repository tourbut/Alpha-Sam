import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import uuid

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_sam"

async def create_data():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Create user (ID=1)
        await session.execute(text("""
            INSERT INTO users (id, email, hashed_password, is_active, is_superuser, is_verified, is_public_leaderboard)
            VALUES (1, 'tester@example.com', 'hashed', true, false, true, false)
            ON CONFLICT (id) DO NOTHING;
        """))
        
        # Create portfolio (ID=1)
        await session.execute(text("""
            INSERT INTO portfolios (id, owner_id, name, currency, visibility, is_primary_for_leaderboard)
            VALUES (1, 1, 'Main Portfolio', 'USD', 'PRIVATE', true)
            ON CONFLICT (id) DO NOTHING;
        """))
        
        # Create asset (ID=1)
        await session.execute(text("""
            INSERT INTO assets (id, owner_id, symbol, name, category)
            VALUES (1, 1, 'BTC', 'Bitcoin', 'Crypto')
            ON CONFLICT (id) DO NOTHING;
        """))
        
        # Create transaction (ID=1)
        await session.execute(text("""
            INSERT INTO transactions (id, portfolio_id, asset_id, type, quantity, price)
            VALUES (1, 1, 1, 'BUY', 1.0, 50000.0)
            ON CONFLICT (id) DO NOTHING;
        """))

        await session.commit()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_data())
