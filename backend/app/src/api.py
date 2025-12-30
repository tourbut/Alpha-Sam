from fastapi import APIRouter
from app.src.routes import assets, prices, positions, auth, users, portfolio, transactions, market, user_settings

api_router = APIRouter()

# FastAPI Users Integration
from app.src.core.users_config import fastapi_users, auth_backend
from app.src.schemas.user import UserRead, UserCreate, UserUpdate

# 1. Auth Router (Login) - /api/v1/auth/jwt/login
api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

# 2. Register Router - /api/v1/auth/register
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# 3. Users Router - /api/v1/users (Provides /users/me, /users/{id})
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Manual Routers (Commented out conflicting ones, kept others)
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) # Replaced by FastAPI Users logic
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
# api_router.include_router(users.router, prefix="/users", tags=["users"]) # Replaced/Merged by FastAPI Users
api_router.include_router(user_settings.router, prefix="/users", tags=["users"]) # Keep settings if distinct
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
