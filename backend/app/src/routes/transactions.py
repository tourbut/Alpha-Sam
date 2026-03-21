from typing import Any
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.src.crud import transactions as crud_transaction
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter()

@router.post("", response_model=TransactionRead)
async def create_transaction(*, 
    transaction_in: TransactionCreate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    거래 내역 생성 (포지션 자동 업데이트)
    """
    from app.src.services.transaction_service import TransactionService
    return await TransactionService.create_transaction(session, transaction_in.dict())

@router.get("", response_model=List[TransactionRead])
async def read_transactions(*, 
    session: SessionDep_async,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[uuid.UUID] = Query(None, description="특정 자산 필터링")
):
    """
    거래 내역 목록 조회
    """
    return await crud_transaction.get_transactions(session=session, owner_id=current_user.id, skip=skip, limit=limit, asset_id=asset_id)

@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(*, 
    transaction_id: uuid.UUID,
    transaction_in: TransactionUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    거래 내역 수정
    """
    tx = await crud_transaction.update_transaction(
        session=session,
        transaction_id=transaction_id,
        transaction_in=transaction_in,
        owner_id=current_user.id,
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found or access denied")
    return tx


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(*, 
    transaction_id: uuid.UUID,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    거래 내역 삭제
    """
    success = await crud_transaction.delete_transaction(
        session=session, transaction_id=transaction_id, owner_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=404, detail="Transaction not found or access denied"
        )
    return None
