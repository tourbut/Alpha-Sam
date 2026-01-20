from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioResponse, PortfolioHistoryRead, PortfolioVisibilityUpdate, PortfolioSharedRead
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
