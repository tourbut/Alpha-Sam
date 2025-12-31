from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.src.core.db import get_session
from app.src.models.position import Position
from app.src.models.asset import Asset
from app.src.models.price import Price
from app.src.models.portfolio_history import PortfolioHistory
from app.src.schemas.position import PositionWithAsset
from app.src.schemas.portfolio import PortfolioResponse, PortfolioSummary, PortfolioStats, PortfolioHistoryRead
from app.src.engine.portfolio_service import calculate_position_metrics, calculate_portfolio_summary
from app.src.crud import crud_portfolio_history
from app.src.deps import get_current_user
from app.src.models.user import User

router = APIRouter()


@router.post("/snapshot", status_code=status.HTTP_201_CREATED)
async def create_portfolio_snapshot(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    현재 포트폴리오 가치 스냅샷 생성 및 저장
    """
    # 1. 모든 포지션 조회 및 가치 계산
    # 1. 모든 포지션 조회
    statement = select(Position).where(Position.owner_id == current_user.id)
    result = await session.execute(statement)
    positions = result.scalars().all()
    
    summary_input_data = []

    if positions:
        # 2. 최신 시세 Batch 조회 (N+1 문제 해결)
        asset_ids = [p.asset_id for p in positions]
        
        # 각 자산별 최신 시세 조회
        # DISTINCT ON (PostgreSQL)을 사용하여 각 자산별 가장 최근 데이터를 가져옴
        price_stmt = (
            select(Price)
            .distinct(Price.asset_id)
            .where(Price.asset_id.in_(asset_ids))
            .order_by(Price.asset_id, desc(Price.timestamp))
        )
        
        price_result = await session.execute(price_stmt)
        latest_prices = price_result.scalars().all()
        
        # asset_id -> price value 매핑
        price_map = {price.asset_id: price.value for price in latest_prices}
    else:
        price_map = {}

    for position in positions:
        current_price = price_map.get(position.asset_id)
        
        summary_input_data.append({
            "quantity": float(position.quantity),
            "buy_price": float(position.buy_price),
            "current_price": current_price
        })

    # 2. 포트폴리오 전체 요약 계산
    summary_metrics = calculate_portfolio_summary(summary_input_data)
    
    # 3. History 저장
    history = PortfolioHistory(
        owner_id=current_user.id,
        total_value=summary_metrics["total_valuation"] or 0.0,
        total_cost=summary_metrics["total_invested"] or 0.0,
        total_pl=summary_metrics["total_profit_loss"] or 0.0
    )
    
    await crud_portfolio_history.create_portfolio_history(session, history)
    
    return {"message": "Snapshot created", "data": history}


@router.get("/summary", response_model=PortfolioResponse)
async def get_portfolio_summary(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포트폴리오 요약 정보 및 전체 포지션 현황 조회
    """
    
    # 1. 모든 포지션 조회 (Asset Eager Loading)
    from sqlalchemy.orm import selectinload
    statement = (
        select(Position)
        .where(Position.owner_id == current_user.id)
        .options(selectinload(Position.asset))
    )
    result = await session.execute(statement)
    positions = result.scalars().all()
    
    if not positions:
        return PortfolioResponse(
            summary=PortfolioSummary(
                total_value=0.0,
                total_cost=0.0,
                total_pl=0.0,
                total_pl_stats=PortfolioStats(percent=0.0, direction="flat")
            ),
            positions=[]
        )

    # 2. 최신 시세 Batch 조회
    # 각 자산별 최신 시세를 한 번의 쿼리로 가져오기 위해 Window Function 등 사용 가능하나,
    # 간단하게 asset_id 목록으로 IN 쿼리 후 Python에서 매핑
    asset_ids = [p.asset_id for p in positions]
    
    # 각 자산별 가장 최근 Price 조회 (DISTINCT ON 사용 - PostgreSQL 전용)
    # 또는 MAX(timestamp) GROUP BY asset_id 서브쿼리 사용
    # 여기서는 간단히 모든 관련 Price 중 최근 N개를 가져와서 필터링 (데이터 양이 많지 않다고 가정)
    # 하지만 Price 데이터가 많으므로 DISTINCT ON을 사용하는 것이 효율적
    
    price_stmt = (
        select(Price)
        .distinct(Price.asset_id)
        .where(Price.asset_id.in_(asset_ids))
        .order_by(Price.asset_id, desc(Price.timestamp))
    )
    
    price_result = await session.execute(price_stmt)
    latest_prices = price_result.scalars().all()
    
    # asset_id -> price value 매핑
    price_map = {price.asset_id: price.value for price in latest_prices}
    
    position_reads: List[PositionWithAsset] = []
    summary_input_data = []

    for position in positions:
        asset = position.asset
        current_price = price_map.get(position.asset_id)
        
        # 수익률 계산
        metrics = calculate_position_metrics(
            quantity=position.quantity,
            buy_price=position.buy_price,
            current_price=current_price
        )
        
        # 1-1. PositionWithAsset 생성
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
        
        # 1-2. Summary 계산용 데이터 수집
        summary_input_data.append({
            "quantity": float(position.quantity),
            "buy_price": float(position.buy_price),
            "current_price": current_price
        })

    # 3. 포트폴리오 전체 요약 계산
    summary_metrics = calculate_portfolio_summary(summary_input_data)
    
    total_pl = summary_metrics["total_profit_loss"]
    
    # 방향 결정
    direction = "flat"
    if total_pl is not None:
        if total_pl > 0:
            direction = "up"
        elif total_pl < 0:
            direction = "down"

    summary_schema = PortfolioSummary(
        total_value=summary_metrics["total_valuation"],
        total_cost=summary_metrics["total_invested"],
        total_pl=summary_metrics["total_profit_loss"],
        total_pl_stats=PortfolioStats(
            percent=summary_metrics["portfolio_return_rate"],
            direction=direction
        )
    )

    return PortfolioResponse(
        summary=summary_schema,
        positions=position_reads
    )


@router.get("/history", response_model=List[PortfolioHistoryRead])
async def read_portfolio_history(
    skip: int = 0,
    limit: int = 30,  # Default to 30 for chart
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    포트폴리오 히스토리 조회
    """
    return await crud_portfolio_history.get_portfolio_history(session, owner_id=current_user.id, skip=skip, limit=limit)
