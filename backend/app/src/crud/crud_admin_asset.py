from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.admin import AdminAsset
from app.src.schemas.admin_asset import AdminAssetCreate

class CRUDAdminAsset:
    async def get(self, db: AsyncSession, id: UUID) -> Optional[AdminAsset]:
        return await db.get(AdminAsset, id)

    async def get_by_symbol(self, db: AsyncSession, symbol: str) -> Optional[AdminAsset]:
        statement = select(AdminAsset).where(AdminAsset.symbol == symbol)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AdminAsset]:
        statement = select(AdminAsset).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_all_active(self, db: AsyncSession) -> List[AdminAsset]:
        statement = select(AdminAsset).where(AdminAsset.is_active == True)
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: AdminAssetCreate) -> AdminAsset:
        db_obj = AdminAsset.model_validate(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: UUID) -> Optional[AdminAsset]:
        obj = await db.get(AdminAsset, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def toggle_active(self, db: AsyncSession, id: UUID) -> Optional[AdminAsset]:
        obj = await db.get(AdminAsset, id)
        if obj:
            obj.is_active = not obj.is_active
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
        return obj

admin_asset = CRUDAdminAsset()
