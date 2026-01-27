from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.admin_asset import AdminAssetCreate, AdminAssetRead
from app.src.models.admin import AdminAsset
from app.src.crud.crud_admin_asset import admin_asset
from app.src.core.db import get_session
from app.src.deps import get_current_superuser

router = APIRouter()

@router.get("/assets", response_model=List[AdminAssetRead])
async def read_admin_assets(
    *,
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_superuser = Depends(get_current_superuser)
):
    """
    [Admin Only] 관리 대상 자산 목록 조회
    """
    return await admin_asset.get_multi(session, skip=skip, limit=limit)

@router.post("/assets", response_model=AdminAssetRead)
async def create_admin_asset(
    *,
    session: AsyncSession = Depends(get_session),
    asset_in: AdminAssetCreate,
    current_superuser = Depends(get_current_superuser)
):
    """
    [Admin Only] 관리 대상 자산 추가
    """
    # 중복 체크
    if await admin_asset.get_by_symbol(session, asset_in.symbol):
        raise HTTPException(
            status_code=400,
            detail="The asset with this symbol already exists in the system."
        )
    
    asset = await admin_asset.create(session, asset_in)
    return asset

@router.delete("/assets/{asset_id}", response_model=AdminAssetRead)
async def delete_admin_asset(
    *,
    session: AsyncSession = Depends(get_session),
    asset_id: UUID,
    current_superuser = Depends(get_current_superuser)
):
    """
    [Admin Only] 관리 대상 자산 삭제
    """
    asset = await admin_asset.remove(session, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/assets/{asset_id}/toggle", response_model=AdminAssetRead)
async def toggle_admin_asset(
    *,
    session: AsyncSession = Depends(get_session),
    asset_id: UUID,
    current_superuser = Depends(get_current_superuser)
):
    """
    [Admin Only] 자산 활성화/비활성화 토글
    """
    asset = await admin_asset.toggle_active(session, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
