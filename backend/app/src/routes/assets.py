from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.db import get_session
from app.src.schemas.asset import AssetCreate, AssetRead
from app.src.engine.portfolio_service import calculate_position_metrics
from app.src.crud import crud_asset
from app.src.engine.price_service import price_service
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
    # CRUD 레이어에서 데이터 가져오기 (Asset, Price, Position 관련 데이터 포함)
    assets_data = await crud_asset.get_assets(session, owner_id=current_user.id, skip=skip, limit=limit)
    
    asset_reads = []
    for asset, latest_price, latest_timestamp, position_obj in assets_data:
        asset_read = AssetRead.model_validate(asset)
        
        if latest_price is not None:
            asset_read.latest_price = latest_price
            asset_read.latest_price_updated_at = latest_timestamp
        
        # Position이 있으면 계산된 메트릭 포함
        if position_obj:
            current_price_for_calc = latest_price
            metrics = calculate_position_metrics(
                quantity=position_obj.quantity,
                buy_price=position_obj.buy_price,
                current_price=current_price_for_calc
            )
            asset_read.valuation = metrics["valuation"]
            asset_read.profit_loss = metrics["profit_loss"]
            asset_read.return_rate = metrics["return_rate"]
        else:
            asset_read.valuation = None
            asset_read.profit_loss = None
            asset_read.return_rate = None
            
        asset_reads.append(asset_read)

    return asset_reads

@router.post("/", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_in: AssetCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    신규 자산 등록 (Multi-tenancy 적용)
    """
    # 해당 사용자가 이 심볼의 자산을 이미 가지고 있는지 또는 글로벌 자산이 있는지 확인
    # (여기서의 정책: 동일한 심볼의 자산은 사용자별로 1개 또는 글로벌 1개만 가능)
    # 일단 심볼 중복 체크 (글로벌 또는 본인 자산 중)
    # crud_asset.get_asset_by_symbol 를 수정하거나 여기서 필터링
    existing_asset = await crud_asset.get_asset_by_symbol(session, symbol=asset_in.symbol)
    if existing_asset and (existing_asset.owner_id is None or existing_asset.owner_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Asset with symbol {asset_in.symbol} already exists"
        )
    
    # Auto-fill name/category if missing
    if not asset_in.name:
        results = await price_service.search_symbol(asset_in.symbol)
        match = next((r for r in results if r["symbol"] == asset_in.symbol.upper()), None)
        if not match and results:
            match = results[0]
            
        if match:
            asset_in.name = match["name"]
            if not asset_in.category and match.get("type"):
                asset_in.category = match["type"]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Name is required (could not auto-fill from symbol)"
            )

    # 소유자 설정
    asset_in.owner_id = current_user.id if asset_in.owner_id is None else asset_in.owner_id

    return await crud_asset.create_asset(session, obj_in=asset_in)

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

