from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioResponse, PortfolioHistoryRead, PortfolioVisibilityUpdate, PortfolioSharedRead, PortfolioWithAssetsSummary
from app.src.schemas.transaction import TransactionCreate, TransactionRead
from app.src.engine.portfolio_service import portfolio_service_instance
from app.src.services.portfolio_service import PortfolioService
from app.src.deps import SessionDep_async, CurrentUser
from app.src.crud import crud_portfolio_history

router = APIRouter(tags=["portfolios"])

@router.post("", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio_in: PortfolioCreate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    새 포트폴리오 생성
    """
    return await portfolio_service_instance.create_portfolio(
        session=db,
        owner_id=current_user.id,
        name=portfolio_in.name,
        description=portfolio_in.description
    )

@router.get("", response_model=List[PortfolioRead])
async def read_portfolios(
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    내 포트폴리오 목록 조회
    """
    return await portfolio_service_instance.get_user_portfolios(session=db, owner_id=current_user.id)

@router.get("/with-assets", response_model=List[PortfolioWithAssetsSummary])
async def read_portfolios_with_assets(
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 목록 + 자산 요약 정보 조회
    
    각 포트폴리오에 대해 다음 정보를 반환합니다:
    - 기본 정보 (id, name, description, created_at)
    - 총 평가금액 (total_value)
    - 자산 구성 리스트 (symbol, name, value, percentage)
    """
    return await PortfolioService.get_portfolios_with_assets(session=db, user_id=current_user.id)

# Merged from portfolio.py (singular)
@router.post("/snapshot", status_code=status.HTTP_201_CREATED)
async def create_portfolio_snapshot(
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    현재 포트폴리오 가치 스냅샷 생성 및 저장
    """
    history = await PortfolioService.create_snapshot(session, current_user.id)
    return {"message": "Snapshot created", "data": history}

@router.get("/summary", response_model=PortfolioResponse)
async def get_portfolio_summary(
    session: SessionDep_async,
    current_user: CurrentUser,
    portfolio_id: Optional[uuid.UUID] = None
):
    """
    포트폴리오 요약 정보 및 전체 포지션 현황 조회
    """
    return await PortfolioService.get_summary(session, current_user.id, portfolio_id)

@router.get("/history", response_model=List[PortfolioHistoryRead])
async def read_portfolio_history(
    skip: int = 0,
    limit: int = 30,
    session: SessionDep_async = None,
    current_user: CurrentUser = None
):
    """
    포트폴리오 히스토리 조회
    """
    return await crud_portfolio_history.get_portfolio_history(session=session, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def read_portfolio(
    portfolio_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 상세 조회
    """
    portfolio = await portfolio_service_instance.get_portfolio(
        session=db, 
        portfolio_id=portfolio_id, 
        owner_id=current_user.id
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

from app.src.schemas.position import PositionRead

@router.get("/{portfolio_id}/positions", response_model=List[PositionRead])
async def read_portfolio_positions(
    portfolio_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오의 포지션 목록 조회
    """
    # Verify ownership
    portfolio = await portfolio_service_instance.get_portfolio(db, portfolio_id, current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    return await portfolio_service_instance.get_portfolio_positions(session=db, portfolio_id=portfolio_id)

@router.patch("/{portfolio_id}/visibility", response_model=PortfolioRead)
async def update_portfolio_visibility(
    portfolio_id: uuid.UUID,
    visibility_in: PortfolioVisibilityUpdate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 공개 범위 설정 변경
    """
    # Verify ownership
    portfolio = await portfolio_service_instance.get_portfolio(db, portfolio_id, current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    updated_portfolio = await PortfolioService.update_visibility(db, portfolio_id, visibility_in.visibility)
    return updated_portfolio

@router.get("/shared/{token}", response_model=PortfolioSharedRead)
async def read_shared_portfolio(
    token: uuid.UUID,
    db: SessionDep_async
):
    """
    공유 링크(Token)로 포트폴리오 조회 (로그인 불필요)
    """
    portfolio_shared = await PortfolioService.get_shared_portfolio(db, token)
    if not portfolio_shared:
        raise HTTPException(status_code=404, detail="Shared portfolio not found or not accessible")
    return portfolio_shared

@router.post("/{portfolio_id}/transactions", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    portfolio_id: uuid.UUID,
    tx_in: TransactionCreate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    거래 내역 추가 (및 포지션 자동 갱신)
    """
    # Verify ownership
    portfolio = await portfolio_service_instance.get_portfolio(db, portfolio_id, current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    from datetime import datetime
    
    # executed_at 필드 처리: 문자열을 datetime 객체로 변환
    if tx_in.executed_at:
        try:
            # ISO 8601 형식 문자열을 datetime 객체로 변환
            # "2026-01-12" 형식은 date만 포함하므로 시간 부분을 추가
            if 'T' not in tx_in.executed_at:
                # Date만 있는 경우 00:00:00 시간 추가
                executed_at = datetime.fromisoformat(tx_in.executed_at + "T00:00:00")
            else:
                executed_at = datetime.fromisoformat(tx_in.executed_at)
        except Exception:
            # 파싱 실패 시 현재 시각 사용
            executed_at = datetime.utcnow()
    else:
        executed_at = datetime.utcnow()
    
    try:
        tx = await portfolio_service_instance.add_transaction(
            session=db,
            portfolio_id=portfolio_id,
            asset_id=tx_in.asset_id,
            type=tx_in.type,
            quantity=tx_in.quantity,
            price=tx_in.price,
            executed_at=executed_at
        )
        return tx
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# 개별 자산 관련 엔드포인트 (신규)
# ============================================

from app.src.schemas.position import AssetSummaryRead
from app.src.schemas.transaction import TransactionWithDetails
from app.src.models.transaction import Transaction
from app.src.models.price import Price
from sqlalchemy import select, desc


@router.get("/{portfolio_id}/assets/{asset_id}", response_model=AssetSummaryRead)
async def read_portfolio_asset_summary(
    portfolio_id: uuid.UUID,
    asset_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 내 개별 자산의 요약 정보 조회
    
    - symbol: 자산 심볼
    - name: 자산 이름
    - quantity: 총 보유량
    - avgPrice: 평균 매수가
    - currentPrice: 현재가 (가격 정보 있는 경우)
    - totalValue: 평가금액
    - profitLoss: 손익
    - returnRate: 수익률 (%)
    """
    # 1. 포트폴리오 소유권 확인
    portfolio = await portfolio_service_instance.get_portfolio(db, portfolio_id, current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # 2. 해당 포트폴리오의 positions 조회 (Transaction 기반 계산)
    positions = await portfolio_service_instance.get_portfolio_positions(session=db, portfolio_id=portfolio_id)
    
    # 3. 특정 asset_id 필터링
    target_position = None
    for pos in positions:
        if pos.asset_id == asset_id:
            target_position = pos
            break
    
    if not target_position:
        raise HTTPException(status_code=404, detail="Asset not found in this portfolio")
    
    # 4. 현재 가격 조회
    price_stmt = (
        select(Price)
        .where(Price.asset_id == asset_id)
        .order_by(desc(Price.timestamp))
        .limit(1)
    )
    price_result = await db.execute(price_stmt)
    latest_price = price_result.scalar_one_or_none()
    
    current_price = float(latest_price.value) if latest_price else None
    
    # 5. 평가금액 및 손익 계산
    if current_price is not None:
        total_value = target_position.quantity * current_price
        profit_loss = (current_price - target_position.avg_price) * target_position.quantity
        return_rate = ((current_price - target_position.avg_price) / target_position.avg_price * 100) if target_position.avg_price > 0 else 0.0
    else:
        # 현재가 없으면 평균 매수가 기준
        total_value = target_position.quantity * target_position.avg_price
        profit_loss = 0.0
        return_rate = 0.0
    
    return AssetSummaryRead(
        asset_id=target_position.asset_id,
        symbol=target_position.asset_symbol or "UNKNOWN",
        name=target_position.asset_name or "Unknown Asset",
        quantity=target_position.quantity,
        avg_price=target_position.avg_price,
        current_price=current_price,
        total_value=round(total_value, 2),
        profit_loss=round(profit_loss, 2),
        return_rate=round(return_rate, 2)
    )


@router.get("/{portfolio_id}/assets/{asset_id}/transactions", response_model=List[TransactionWithDetails])
async def read_asset_transactions(
    portfolio_id: uuid.UUID,
    asset_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 내 개별 자산의 거래 내역 조회
    
    - id: 거래 ID
    - type: 거래 유형 ("buy" 또는 "sell")
    - date: 거래 일시
    - quantity: 거래 수량
    - price: 거래 단가
    - total: 총 거래금액 (quantity * price)
    - fee: 수수료 (현재 null, 향후 확장)
    """
    # 1. 포트폴리오 소유권 확인
    portfolio = await portfolio_service_instance.get_portfolio(db, portfolio_id, current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # 2. 해당 자산의 거래 내역 조회
    stmt = (
        select(Transaction)
        .where(
            Transaction.portfolio_id == portfolio_id,
            Transaction.asset_id == asset_id
        )
        .order_by(desc(Transaction.executed_at))
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()
    
    # 3. 응답 형식으로 변환
    tx_list = []
    for tx in transactions:
        tx_detail = TransactionWithDetails(
            id=tx.id,
            type=tx.type.lower(),  # "BUY" -> "buy", "SELL" -> "sell"
            date=tx.executed_at,
            quantity=float(tx.quantity),
            price=float(tx.price),
            total=round(float(tx.quantity) * float(tx.price), 2),
            fee=None  # 현재 모델에 fee 필드 없음
        )
        tx_list.append(tx_detail)
    
    return tx_list

