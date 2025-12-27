from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.models.user import User
from app.src.schemas.user import UserCreate, UserUpdate
from app.src.core import security

async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)

async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=security.get_password_hash(obj_in.password),
        is_active=True
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj

async def update_user(session: AsyncSession, db_user: User, obj_in: UserUpdate) -> User:
    users_data = obj_in.model_dump(exclude_unset=True)
    for field, value in users_data.items():
        setattr(db_user, field, value)
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def update_user_password(session: AsyncSession, db_user: User, password: str) -> User:
    """
    Update user password, assumes hashing is handled or handle it here?
    Typically CRUD is low level. But to keep crud_user atomic for user updates.
    """
    # Assuming the caller hashes it? Or should we hash here?
    # Security best practice: CRUD should probably handle raw input or domain model? 
    # Let's handle generic DB update. 
    # But for safety, let's say this method takes plain text and hashes it, 
    # OR takes hashed password. 
    # Given `create_user` hashes internally, `update_user_password` should probably check existing password? 
    # No, verification is business/API logic. CRUD is persistence.
    # Let's take new_hashed_password.
    db_user.hashed_password = password
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def authenticate(session: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user
