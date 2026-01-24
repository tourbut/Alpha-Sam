from typing import List
import uuid
from fastapi import APIRouter, Depends
from app.src.deps import SessionDep_async, CurrentUser
from app.src.schemas.dashboard import ActivityItem, ActivityType
from app.src.crud import portfolios as crud_portfolio
from app.src.crud import assets as crud_asset
from app.src.crud import transactions as crud_transaction

router = APIRouter(tags=["dashboard"])

@router.get("/activities", response_model=List[ActivityItem])
async def get_recent_activities(
    current_user: CurrentUser,
    db: SessionDep_async
):
    """
    대시보드: 최근 활동 (Recent Activity) 조회
    
    사용자의 최근 활동 (포트폴리오 생성, 자산 추가, 거래 내역)을 
    생성일시(executed_at 또는 created_at) 기준으로 통합하여 상위 5개를 반환합니다.
    """
    
    # 1. Recent Portfolios (Created)
    portfolios = await crud_portfolio.get_recent_portfolios(session=db, owner_id=current_user.id, limit=5)
    
    # 2. Recent Assets (Added)
    assets = await crud_asset.get_recent_assets(session=db, owner_id=current_user.id, limit=5)
    
    # 3. Recent Transactions (Executed)
    transactions = await crud_transaction.get_recent_transactions(session=db, owner_id=current_user.id, limit=5)
    
    # 4. Integrate & Map to ActivityItem
    activities = []
    
    # Map Portfolios
    for p in portfolios:
        activities.append(ActivityItem(
            id=uuid.uuid4(), # Generate temporary ID for the activity item itself
            type=ActivityType.PORTFOLIO_CREATED,
            title=f"New Portfolio: {p.name}",
            description=f"Created portfolio '{p.name}'",
            timestamp=p.created_at,
            entity_id=p.id,
            portfolio_id=p.id
        ))
        
    # Map Assets
    for a in assets:
        activities.append(ActivityItem(
            id=uuid.uuid4(),
            type=ActivityType.ASSET_ADDED,
            title=f"Added Asset: {a.symbol}",
            description=f"Added {a.name} ({a.symbol})",
            timestamp=a.created_at,
            entity_id=a.id,
            portfolio_id=a.portfolio_id
        ))
        
    # Map Transactions
    for t in transactions:
        verb = "Bought" if t.type.upper() == "BUY" else "Sold"
        activities.append(ActivityItem(
            id=uuid.uuid4(),
            type=ActivityType.TRANSACTION_EXECUTED,
            title=f"{verb} Asset",
            description=f"{verb} {t.quantity} unit(s) at {t.price}",
            timestamp=t.executed_at,
            entity_id=t.id,
            portfolio_id=t.portfolio_id
        ))

    # 5. Sort by timestamp descending
    activities.sort(key=lambda x: x.timestamp, reverse=True)
    
    # 6. Return top 5
    return activities[:5]
