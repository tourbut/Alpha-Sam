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

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(
    position_in: PositionCreate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    새 포지션 생성
    """
    # 1. 이미 존재하는지 확인
    existing_position = await crud_position.get_position_by_asset(
        session=session, asset_id=position_in.asset_id, owner_id=current_user.id
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
    return await crud_position.create_position(session=session, position_in=new_position)

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

@router.put("/{position_id}", response_model=PositionRead)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    포지션 수정
    """
    position = await crud_position.get_position(session=session, position_id=position_id, owner_id=current_user.id)
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
        
    update_data = position_in.model_dump(exclude_unset=True)
    return await crud_position.update_position(session=session, position=position, update_data=update_data)

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    session: SessionDep_async,
    current_user: CurrentUser
):
    """
    포지션 삭제
    """
    position = await crud_position.get_position(session=session, position_id=position_id, owner_id=current_user.id)
    
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
        
    await crud_position.remove_position(session=session, position=position)
