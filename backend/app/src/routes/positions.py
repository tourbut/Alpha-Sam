from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.schemas.position import PositionCreate, PositionRead, PositionUpdate
from app.src.models.position import Position
from app.src.crud import crud_position
from app.src.deps import SessionDep_async, CurrentUser

router = APIRouter()

@router.get("/", response_model=List[PositionRead])
async def read_positions(
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    현재 사용자의 모든 포지션 조회
    """
    return await crud_position.get_positions(session=session, owner_id=current_user.id)

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_position(
    position_in: PositionCreate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    [DEPRECATED] Manual position creation is disabled. Use Transaction API instead.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Manual position creation is disabled. Please use the Transaction API (BUY/SELL)."
    )

@router.get("/{position_id}", response_model=PositionRead)
async def read_position(
    position_id: int,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    특정 포지션 조회
    """
    position = await crud_position.get_position(session=session, position_id=position_id, owner_id=current_user.id)
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    return position

@router.put("/{position_id}", response_model=PositionRead, include_in_schema=False)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    [DEPRECATED] Manual position update is disabled. Use Transaction API instead.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Manual position modification is disabled. Please use the Transaction API (BUY/SELL)."
    )

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
async def delete_position(
    position_id: int,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    [DEPRECATED] Manual position deletion is disabled.
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Manual position deletion is disabled. Assets are managed via Transactions."
    )
