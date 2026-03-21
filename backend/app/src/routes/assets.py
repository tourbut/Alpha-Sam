from typing import Any
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.db import get_session
from app.src.schemas.asset import AssetCreate, AssetRead, AssetUpdate
import app.src.schemas.asset # lazy import fix or direct import
from app.src.services.asset_service import asset_service
from app.src.crud import assets as crud_asset
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter()

@router.get("", response_model=List[AssetRead])
async def read_assets(*, 
    skip: int = 0,
    limit: int = 100,
    session: SessionDep_async = None, # Default None to silence linter if needed, but Depends handles it
    current_user: CurrentUser = None
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

@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(*, 
    asset_in: AssetCreate,
    session: SessionDep_async,
    current_user: CurrentUser
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
async def delete_asset(*, 
    asset_id: uuid.UUID,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    자산 삭제 (Security Check: 본인 것만 삭제 가능)
    """
    asset = await crud_asset.get_asset(session=session, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot delete global or other users' assets")

    return await crud_asset.remove_asset(session=session, asset_id=asset_id)


@router.put("/{asset_id}", response_model=AssetRead)
async def update_asset(*, 
    asset_id: uuid.UUID,
    asset_in: app.src.schemas.asset.AssetUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    자산 정보 수정 (본인 소유 자산만)
    """
    asset = await crud_asset.update_asset(session=session, asset_id=asset_id, asset_in=asset_in, owner_id=current_user.id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found or access denied")
    return asset
