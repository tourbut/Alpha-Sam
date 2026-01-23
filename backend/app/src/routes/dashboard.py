from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from app.src.deps import SessionDep_async, CurrentUser
from app.src.schemas.dashboard import ActivityItem, ActivityType
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.transaction import Transaction

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
    portfolio_stmt = (
        select(Portfolio)
        .where(Portfolio.owner_id == current_user.id)
        .order_by(desc(Portfolio.created_at))
        .limit(5)
    )
    portfolios_result = await db.execute(portfolio_stmt)
    portfolios = portfolios_result.scalars().all()
    
    # 2. Recent Assets (Added)
    # Asset has owner_id, so we can filter by that.
    asset_stmt = (
        select(Asset)
        .where(Asset.owner_id == current_user.id)
        .order_by(desc(Asset.created_at))
        .limit(5)
    )
    assets_result = await db.execute(asset_stmt)
    assets = assets_result.scalars().all()
    
    # 3. Recent Transactions (Executed)
    # Transaction doesn't have owner_id directly but links to Portfolio which has owner_id.
    # We join Portfolio to filter by owner.
    transaction_stmt = (
        select(Transaction)
        .join(Portfolio)
        .where(Portfolio.owner_id == current_user.id)
        .order_by(desc(Transaction.executed_at))
        .limit(5)
    )
    transactions_result = await db.execute(transaction_stmt)
    transactions = transactions_result.scalars().all()
    
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
        # Pre-fetch asset symbol if possible, or use placeholder. 
        # In a real scenario, we might want to eagerly load 'asset' relationship.
        # Here we'll do a simple string format.
        # Since we didn't eager load, accessing t.asset might trigger lazy load error or be missing.
        # For performance, let's assume simple description for now.
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
