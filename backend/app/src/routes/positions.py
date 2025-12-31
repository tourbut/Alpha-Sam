"""
Position (보유 내역) API 엔드포인트
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.src.core.db import get_session
from app.src.models.position import Position
from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.schemas.position import PositionCreate, PositionRead, PositionUpdate, PositionWithAsset
from app.src.engine.portfolio_service import calculate_position_metrics
from app.src.deps import get_current_user
from app.src.models.user import User

router = APIRouter()


@router.get("/", response_model=List[PositionWithAsset])
async def read_positions(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포지션 목록 조회 (Asset 정보 및 계산된 메트릭 포함)
    """
    statement = select(Position).where(Position.owner_id == current_user.id).offset(skip).limit(limit)
    result = await session.execute(statement)
    positions = result.scalars().all()
    
    position_reads = []
    for position in positions:
        # Asset 정보 조회
        asset_stmt = select(Asset).where(Asset.id == position.asset_id)
        asset_result = await session.execute(asset_stmt)
        asset = asset_result.scalar_one_or_none()
        
        # Asset이 삭제된 경우 처리
        if not asset:
            # Asset이 없어도 Position 정보는 반환하되, Asset 정보는 None
            asset = None
        
        # 최신 시세 조회
        price_stmt = (
            select(Price)
            .where(Price.asset_id == position.asset_id)
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        price_result = await session.execute(price_stmt)
        latest_price_obj = price_result.scalar_one_or_none()
        current_price = latest_price_obj.value if latest_price_obj else None
        
        # 수익률 계산 (시세가 없으면 None 반환)
        metrics = calculate_position_metrics(
            quantity=position.quantity,
            buy_price=position.buy_price,
            current_price=current_price
        )
        
        # PositionRead 생성
        position_dict = {
            "id": position.id,
            "asset_id": position.asset_id,
            "quantity": float(position.quantity),
            "buy_price": float(position.buy_price),
            "buy_date": position.buy_date,
            "created_at": position.created_at,
            "updated_at": position.updated_at,
            "valuation": metrics["valuation"],
            "profit_loss": metrics["profit_loss"],
            "return_rate": metrics["return_rate"],
            "current_price": current_price,
            "asset_symbol": asset.symbol if asset else None,
            "asset_name": asset.name if asset else None,
            "asset_category": asset.category if asset else None,
        }
        position_reads.append(PositionWithAsset(**position_dict))
    
    return position_reads


@router.get("/{position_id}", response_model=PositionWithAsset)
async def read_position(
    position_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    특정 포지션 조회
    """
    statement = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(statement)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Position with id {position_id} not found"
        )
    
    # Asset 정보 조회
    asset_stmt = select(Asset).where(Asset.id == position.asset_id)
    asset_result = await session.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    
    # Asset이 삭제된 경우 처리
    if not asset:
        # Asset이 없어도 Position 정보는 반환하되, Asset 정보는 None
        asset = None
    
    # 최신 시세 조회
    price_stmt = (
        select(Price)
        .where(Price.asset_id == position.asset_id)
        .order_by(desc(Price.timestamp))
        .limit(1)
    )
    price_result = await session.execute(price_stmt)
    latest_price_obj = price_result.scalar_one_or_none()
    current_price = latest_price_obj.value if latest_price_obj else None
    
    # 수익률 계산 (시세가 없으면 None 반환)
    metrics = calculate_position_metrics(
        quantity=position.quantity,
        buy_price=position.buy_price,
        current_price=current_price
    )
    
    position_dict = {
        "id": position.id,
        "asset_id": position.asset_id,
        "quantity": float(position.quantity),
        "buy_price": float(position.buy_price),
        "buy_date": position.buy_date,
        "created_at": position.created_at,
        "updated_at": position.updated_at,
        "valuation": metrics["valuation"],
        "profit_loss": metrics["profit_loss"],
        "return_rate": metrics["return_rate"],
        "current_price": current_price,
        "asset_symbol": asset.symbol if asset else None,
        "asset_name": asset.name if asset else None,
        "asset_category": asset.category if asset else None,
    }
    return PositionWithAsset(**position_dict)


@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(
    position_in: PositionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포지션 생성 (유효성 검증: quantity >= 0, buy_price > 0)
    """
    # 유효성 검증 (Pydantic 스키마에서도 검증하지만, 명시적으로 재확인)
    if position_in.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="quantity must be greater than or equal to 0"
        )
    
    if position_in.buy_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="buy_price must be greater than 0"
        )
    
    # quantity가 0이면 경고는 하지만 허용 (과거 이력 보존 목적)
    if position_in.quantity == 0:
        # 0 수량은 사실상 보유하지 않는 것으로 처리 가능하지만, 생성은 허용
        pass
    
    # Asset 존재 확인
    asset_stmt = select(Asset).where(Asset.id == position_in.asset_id)
    asset_result = await session.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with id {position_in.asset_id} not found. Please create the asset first."
        )
    
    # Position 생성
    db_position = Position(**position_in.model_dump(), owner_id=current_user.id)
    session.add(db_position)
    await session.commit()
    await session.refresh(db_position)
    
    # 최신 시세 조회
    price_stmt = (
        select(Price)
        .where(Price.asset_id == db_position.asset_id)
        .order_by(desc(Price.timestamp))
        .limit(1)
    )
    price_result = await session.execute(price_stmt)
    latest_price_obj = price_result.scalar_one_or_none()
    current_price = latest_price_obj.value if latest_price_obj else None
    
    # 수익률 계산 (시세가 없으면 None 반환, "시세 없음" 상태로 표시)
    metrics = calculate_position_metrics(
        quantity=db_position.quantity,
        buy_price=db_position.buy_price,
        current_price=current_price
    )
    
    position_dict = {
        "id": db_position.id,
        "asset_id": db_position.asset_id,
        "quantity": float(db_position.quantity),
        "buy_price": float(db_position.buy_price),
        "buy_date": db_position.buy_date,
        "created_at": db_position.created_at,
        "updated_at": db_position.updated_at,
        "valuation": metrics["valuation"],
        "profit_loss": metrics["profit_loss"],
        "return_rate": metrics["return_rate"],
        "current_price": current_price,
    }
    return PositionRead(**position_dict)


@router.put("/{position_id}", response_model=PositionRead)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포지션 수정
    """
    statement = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(statement)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Position with id {position_id} not found"
        )
    
    # 업데이트할 필드만 적용
    update_data = position_in.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # 유효성 검증
    if "quantity" in update_data and update_data["quantity"] is not None:
        if update_data["quantity"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="quantity must be greater than or equal to 0"
            )
        position.quantity = update_data["quantity"]
    
    if "buy_price" in update_data and update_data["buy_price"] is not None:
        if update_data["buy_price"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="buy_price must be greater than 0"
            )
        position.buy_price = update_data["buy_price"]
    
    if "buy_date" in update_data:
        position.buy_date = update_data["buy_date"]
    
    await session.commit()
    await session.refresh(position)
    
    # 최신 시세 조회
    price_stmt = (
        select(Price)
        .where(Price.asset_id == position.asset_id)
        .order_by(desc(Price.timestamp))
        .limit(1)
    )
    price_result = await session.execute(price_stmt)
    latest_price_obj = price_result.scalar_one_or_none()
    current_price = latest_price_obj.value if latest_price_obj else None
    
    # 수익률 계산 (시세가 없으면 None 반환, "시세 없음" 상태로 표시)
    metrics = calculate_position_metrics(
        quantity=position.quantity,
        buy_price=position.buy_price,
        current_price=current_price
    )
    
    position_dict = {
        "id": position.id,
        "asset_id": position.asset_id,
        "quantity": float(position.quantity),
        "buy_price": float(position.buy_price),
        "buy_date": position.buy_date,
        "created_at": position.created_at,
        "updated_at": position.updated_at,
        "valuation": metrics["valuation"],
        "profit_loss": metrics["profit_loss"],
        "return_rate": metrics["return_rate"],
        "current_price": current_price,
    }
    return PositionRead(**position_dict)


@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포지션 삭제
    """
    statement = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(statement)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Position with id {position_id} not found"
        )
    
    await session.delete(position)
    await session.commit()
    return None

