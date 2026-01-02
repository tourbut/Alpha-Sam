from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.db import get_session
from app.src.schemas.asset import AssetCreate, AssetRead
from app.src.engine.asset_service import asset_service
from app.src.crud import crud_asset
from app.src.deps import get_current_user
from app.src.models.user import User

router = APIRouter()

@router.get("/", response_model=List[AssetRead])
async def read_assets(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    자산 목록 조회 (최신 시세 포함, Multi-tenancy 적용)
    """
    return await asset_service.get_assets_with_metrics(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.post("/", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_in: AssetCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    신규 자산 등록 (Multi-tenancy 적용)
    """
    return await asset_service.create_asset_with_autofill(
        session=session,
        asset_in=asset_in,
        user_id=current_user.id
    )

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    자산 삭제 (Security Check: 본인 것만 삭제 가능)
    """
    asset = await crud_asset.get_asset(session, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot delete global or other users' assets")

    return await crud_asset.remove_asset(session, asset_id=asset_id)

