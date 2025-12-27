"""
Transaction API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.core.db import get_session
from app.src.schemas.transaction import TransactionCreate, TransactionRead
from app.src.crud import crud_transaction
from app.src.deps import get_current_user
from app.src.models.user import User

router = APIRouter()

@router.post("/", response_model=TransactionRead)
async def create_transaction(
    transaction_in: TransactionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    거래 내역 생성 (포지션 자동 업데이트)
    """
    return await crud_transaction.create_transaction(session, transaction_in, owner_id=current_user.id)

@router.get("/", response_model=List[TransactionRead])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[int] = Query(None, description="특정 자산 필터링"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    거래 내역 목록 조회
    """
    return await crud_transaction.get_transactions(session, owner_id=current_user.id, skip=skip, limit=limit, asset_id=asset_id)
