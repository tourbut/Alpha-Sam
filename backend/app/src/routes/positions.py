from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.core.db import get_db
from app.src.schemas.position import PositionCreate, PositionRead, PositionUpdate
from app.src.schemas.user import UserRead
from app.src.models.position import Position
from app.src.models.user import User
from app.src.core.users_config import current_active_user
from app.src.crud import crud_position

router = APIRouter()

@router.get("/", response_model=List[PositionRead])
async def read_positions(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db)
):
    """
    현재 사용자의 모든 포지션 조회
    """
    stmt = select(Position).where(Position.owner_id == current_user.id)
    result = await session.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(
    position_in: PositionCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db)
):
    """
    새 포지션 생성
    """
    # 1. 이미 존재하는지 확인
    existing_position = await crud_position.get_position_by_asset(
        session, asset_id=position_in.asset_id, owner_id=current_user.id
    )
    if existing_position:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position for this asset already exists. Use update instead."
        )

    # 2. 생성
    new_position = Position(
        **position_in.model_dump(),
        owner_id=current_user.id
    )
    return await crud_position.create_position(session, new_position)

@router.get("/{position_id}", response_model=PositionRead)
async def read_position(
    position_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db)
):
    """
    특정 포지션 조회
    """
    stmt = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    return position

@router.put("/{position_id}", response_model=PositionRead)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db)
):
    """
    포지션 수정
    """
    stmt = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
        
    update_data = position_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(position, field, value)
        
    session.add(position)
    await session.commit()
    await session.refresh(position)
    return position

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db)
):
    """
    포지션 삭제
    """
    stmt = select(Position).where(
        Position.id == position_id,
        Position.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    position = result.scalar_one_or_none()
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
        
    await session.delete(position)
    await session.commit()
