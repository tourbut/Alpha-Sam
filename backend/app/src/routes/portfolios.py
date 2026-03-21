from typing import Any
from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioResponse, PortfolioVisibilityUpdate, PortfolioSharedRead, PortfolioWithAssetsSummary, PortfolioUpdate
from app.src.schemas.transaction import TransactionCreate, TransactionRead
from app.src.schemas.position import PositionRead, AssetSummaryRead, PositionWithAsset
from app.src.schemas.transaction import TransactionWithDetails
from app.src.services.portfolio_service import PortfolioService
from app.src.services.parsers import ParserEngine
from app.src.deps import SessionDep_async, CurrentUser
from app.src.crud import portfolios as crud_portfolio
from app.src.crud import transactions as crud_transaction
from app.src.crud import assets as crud_asset
from app.src.models.prices_day import PriceDay
from sqlalchemy import select, desc
from fastapi import UploadFile, File

router = APIRouter(tags=["portfolios"])

@router.post("", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
async def create_portfolio(*, 
    portfolio_in: PortfolioCreate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    새 포트폴리오 생성
    """
    return await crud_portfolio.create_portfolio(
        session=db,
        owner_id=current_user.id,
        name=portfolio_in.name,
        description=portfolio_in.description
    )

@router.post("/upload/{provider}", status_code=status.HTTP_201_CREATED, response_model=Any)
async def upload_portfolio(*, 
    provider: str,
    current_user: CurrentUser,
    db: SessionDep_async,
    portfolio_id: Optional[uuid.UUID] = None,
    file: UploadFile = File(...)
):
    """
    거래내역 파일을 제공자(provider) 파서를 이용해 파싱하고, 자동생성 포트폴리오에 자산 및 거래를 등록/갱신합니다.
    """
    # 1. 지원하는 파서 조회
    try:
        parser = ParserEngine.get_parser(provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 2. 거래내역 파싱
    try:
        transactions_data = await parser.parse(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if not transactions_data:
        raise HTTPException(status_code=400, detail="No transactions found in the file.")

    # 3. Get or create portfolio
    if portfolio_id:
        portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
    else:
        provider_display_name = provider.capitalize()
        if provider == "toss":
            provider_display_name = "토스증권"
        elif provider == "common":
            provider_display_name = "알파샘 공통양식"
            
        portfolio_name = f"{provider_display_name} 포트폴리오(자동생성)"
        from app.src.models.portfolio import Portfolio
        result = await db.execute(select(Portfolio).where(Portfolio.owner_id == current_user.id, Portfolio.name == portfolio_name))
        portfolio = result.scalars().first()
        
        if not portfolio:
            portfolio = await crud_portfolio.create_portfolio(
                session=db,
                owner_id=current_user.id,
                name=portfolio_name,
                description=f"{provider_display_name} 거래내역 파싱을 통해 자동 생성된 포트폴리오"
            )
    
    # 4. Add transactions
    from app.src.models.asset import Asset
    from app.src.schemas.asset import AssetCreate
    added_count = 0
    for tx in transactions_data:
        if tx.ticker == "UNKNOWN":
            continue
            
        # Get or create asset
        result = await db.execute(
            select(Asset).where(Asset.portfolio_id == portfolio.id, Asset.symbol == tx.ticker)
        )
        asset = result.scalars().first()
        
        if not asset:
            new_asset_data = AssetCreate(
                portfolio_id=portfolio.id,
                owner_id=current_user.id,
                symbol=tx.ticker,
                name=tx.name,
                category="ETF" if "ETF" in tx.name else "Stock"
            )
            asset = await crud_asset.create_asset(session=db, obj_in=new_asset_data)
            
        # Create transaction
        from app.src.models.transaction import Transaction
        db_tx = Transaction(
            portfolio_id=portfolio.id,
            asset_id=asset.id,
            type=tx.type.upper(), # Enum/Calculation 호환성을 위해 대문자 변환
            quantity=tx.quantity,
            price=tx.price,
            executed_at=tx.date
        )
        db.add(db_tx)
        added_count += 1
        
    await db.commit()
    
    return {"message": f"Successfully added {added_count} transactions to portfolio.", "portfolio_id": portfolio.id, "transaction_count": added_count}

@router.get("", response_model=List[PortfolioRead])
async def read_portfolios(*, 
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    내 포트폴리오 목록 조회
    """
    return await crud_portfolio.get_user_portfolios(session=db, owner_id=current_user.id)

@router.get("/with-assets", response_model=List[PortfolioWithAssetsSummary])
async def read_portfolios_with_assets(*, 
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 목록 + 자산 요약 정보 조회
    """
    return await PortfolioService.get_portfolios_with_assets(session=db, user_id=current_user.id)

@router.get("/summary", response_model=PortfolioResponse)
async def get_portfolio_summary(*, 
    session: SessionDep_async,
    current_user: CurrentUser,
    portfolio_id: Optional[uuid.UUID] = None
):
    """
    포트폴리오 요약 정보 및 전체 포지션 현황 조회
    """
    return await PortfolioService.get_summary(session, current_user.id, portfolio_id)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def read_portfolio(*, 
    portfolio_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 상세 조회
    """
    portfolio = await crud_portfolio.get_portfolio(
        session=db, 
        portfolio_id=portfolio_id, 
        owner_id=current_user.id
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.get("/{portfolio_id}/positions", response_model=List[PositionWithAsset])
async def read_portfolio_positions(*, 
    portfolio_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오의 포지션 목록 조회
    """
    # Verify ownership
    portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    return await PortfolioService.get_positions(session=db, portfolio_id=portfolio_id)

@router.patch("/{portfolio_id}/visibility", response_model=PortfolioRead)
async def update_portfolio_visibility(*, 
    portfolio_id: uuid.UUID,
    visibility_in: PortfolioVisibilityUpdate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 공개 범위 설정 변경
    """
    # Verify ownership
    portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    updated_portfolio = await PortfolioService.update_visibility(db, portfolio_id, visibility_in.visibility)
    return updated_portfolio

@router.get("/shared/{token}", response_model=PortfolioSharedRead)
async def read_shared_portfolio(*, 
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
async def create_transaction(*, 
    portfolio_id: uuid.UUID,
    tx_in: TransactionCreate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    거래 내역 추가 (및 포지션 자동 갱신)
    """
    # Force portfolio_id from path to ensure consistency
    tx_in.portfolio_id = portfolio_id
    
    # Delegate to CRUD (handles ownership check and creation)
    return await crud_transaction.create_transaction(
        session=db,
        transaction_in=tx_in,
        owner_id=current_user.id
    )

@router.get("/{portfolio_id}/assets/{asset_id}", response_model=AssetSummaryRead)
async def read_portfolio_asset_summary(*, 
    portfolio_id: uuid.UUID,
    asset_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 내 개별 자산의 요약 정보 조회
    """
    # 1. 포트폴리오 소유권 확인
    portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # 2. 해당 포트폴리오의 positions 조회 (via Service)
    positions = await PortfolioService.get_positions(session=db, portfolio_id=portfolio_id)
    
    # 3. 특정 asset_id 필터링
    target_position = None
    for pos in positions:
        if pos.asset_id == asset_id:
            target_position = pos
            break
    
    if not target_position:
        raise HTTPException(status_code=404, detail="Asset not found in this portfolio")
    
    # Service already enriched price and metrics
    return AssetSummaryRead(
        asset_id=target_position.asset_id,
        symbol=target_position.asset_symbol or "UNKNOWN",
        name=target_position.asset_name or "Unknown Asset",
        quantity=target_position.quantity,
        avg_price=target_position.avg_price,
        current_price=target_position.current_price,
        total_value=round(target_position.valuation or 0.0, 2),
        profit_loss=round(target_position.profit_loss or 0.0, 2),
        return_rate=round(target_position.return_rate or 0.0, 2)
    )

@router.get("/{portfolio_id}/assets/{asset_id}/transactions", response_model=List[TransactionWithDetails])
async def read_asset_transactions(*, 
    portfolio_id: uuid.UUID,
    asset_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    특정 포트폴리오 내 개별 자산의 거래 내역 조회
    """
    # 1. 포트폴리오 소유권 확인 (Optional since crud checks it, but good for explicit 404)
    portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # 2. CRUD를 통해 거래 내역 조회
    transactions = await crud_transaction.get_transactions(
        session=db,
        owner_id=current_user.id,
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        limit=1000 # Enough for detail view
    )
    
    # 3. 응답 형식으로 변환
    tx_list = []
    for tx in transactions:
        tx_detail = TransactionWithDetails(
            id=tx.id,
            type=tx.type.lower(),
            date=tx.executed_at,
            quantity=float(tx.quantity),
            price=float(tx.price),
            total=round(float(tx.quantity) * float(tx.price), 2),
            fee=None
        )
        tx_list.append(tx_detail)
    
    return tx_list

@router.put("/{portfolio_id}", response_model=PortfolioRead)
async def update_portfolio(*, 
    portfolio_id: uuid.UUID,
    portfolio_in: PortfolioUpdate,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 수정
    """
    updated_portfolio = await crud_portfolio.update_portfolio(
        session=db, 
        portfolio_id=portfolio_id, 
        portfolio_in=portfolio_in
    )
    return updated_portfolio

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(*, 
    portfolio_id: uuid.UUID,
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    포트폴리오 삭제
    """
    # Verify ownership
    portfolio = await crud_portfolio.get_portfolio(session=db, portfolio_id=portfolio_id, owner_id=current_user.id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    success = await crud_portfolio.delete_portfolio(session=db, portfolio_id=portfolio_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete portfolio")
    return None
