from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.portfolio import PortfolioCreate, PortfolioRead
from app.src.schemas.transaction import TransactionCreate, TransactionRead
from app.src.engine.portfolio_service import portfolio_service_instance
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter(tags=["portfolios"])

@router.post("/", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=List[PortfolioRead])
async def read_portfolios(
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    내 포트폴리오 목록 조회
    """
    return await portfolio_service_instance.get_user_portfolios(session=db, owner_id=current_user.id)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def read_portfolio(
    portfolio_id: int,
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
    portfolio_id: int,
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

@router.post("/{portfolio_id}/transactions", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    portfolio_id: int,
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
    executed_at = tx_in.executed_at if tx_in.executed_at else datetime.utcnow()
    
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
