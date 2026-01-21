import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.src.models.user import User
from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction
# from app.src.crud.crud_user import user_crud
import uuid

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_sam"

async def verify_crud():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("--- CRUD Verification Start ---")
        
        # 1. Create User
        user_in = {"email": f"test_{uuid.uuid4().hex[:8]}@example.com", "hashed_password": "pass"}
        # Note: user_crud might expect different structure, using direct model for safety in test
        new_user = User(**user_in)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"User Created: {new_user.id} (Type: {type(new_user.id)})")
        assert isinstance(new_user.id, uuid.UUID)

        # 2. Create Portfolio
        new_portfolio = Portfolio(
            owner_id=new_user.id,
            name="Test UUID Portfolio",
            visibility=PortfolioVisibility.PRIVATE
        )
        session.add(new_portfolio)
        await session.commit()
        await session.refresh(new_portfolio)
        print(f"Portfolio Created: {new_portfolio.id}, owner_id: {new_portfolio.owner_id}")
        assert isinstance(new_portfolio.id, uuid.UUID)
        assert new_portfolio.owner_id == new_user.id

        # 3. Create Asset
        new_asset = Asset(
            portfolio_id=new_portfolio.id,
            owner_id=new_user.id,
            symbol="ETH",
            name="Ethereum",
            category="Crypto"
        )
        session.add(new_asset)
        await session.commit()
        await session.refresh(new_asset)
        print(f"Asset Created: {new_asset.id}, portfolio_id: {new_asset.portfolio_id}")
        assert isinstance(new_asset.id, uuid.UUID)
        assert new_asset.portfolio_id == new_portfolio.id

        # 4. Create Transaction
        new_tx = Transaction(
            portfolio_id=new_portfolio.id,
            asset_id=new_asset.id,
            type="BUY",
            quantity=10.0,
            price=2000.0
        )
        session.add(new_tx)
        await session.commit()
        await session.refresh(new_tx)
        print(f"Transaction Created: {new_tx.id}, asset_id: {new_tx.asset_id}")
        assert isinstance(new_tx.id, uuid.UUID)
        assert new_tx.asset_id == new_asset.id

        print("--- CRUD Verification Success ---")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(verify_crud())
