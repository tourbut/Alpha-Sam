from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from app.src.models.admin import AdminAsset
from app.src.schemas.admin_asset import AdminAssetCreate

class CRUDAdminAsset:
    def get(self, db: Session, id: UUID) -> Optional[AdminAsset]:
        return db.get(AdminAsset, id)

    def get_by_symbol(self, db: Session, symbol: str) -> Optional[AdminAsset]:
        statement = select(AdminAsset).where(AdminAsset.symbol == symbol)
        return db.exec(statement).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[AdminAsset]:
        statement = select(AdminAsset).offset(skip).limit(limit)
        return db.exec(statement).all()

    def get_all_active(self, db: Session) -> List[AdminAsset]:
        statement = select(AdminAsset).where(AdminAsset.is_active == True)
        return db.exec(statement).all()

    def create(self, db: Session, obj_in: AdminAssetCreate) -> AdminAsset:
        db_obj = AdminAsset.model_validate(obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: UUID) -> Optional[AdminAsset]:
        obj = db.get(AdminAsset, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def toggle_active(self, db: Session, id: UUID) -> Optional[AdminAsset]:
        obj = db.get(AdminAsset, id)
        if obj:
            obj.is_active = not obj.is_active
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

admin_asset = CRUDAdminAsset()
