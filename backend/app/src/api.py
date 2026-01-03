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

# [COMPATIBILITY] Redirect /auth/signup -> /auth/register
# Frontend uses /signup, Backend uses /register.
from fastapi import Request
from fastapi.responses import RedirectResponse

@api_router.post("/auth/signup", tags=["auth"], include_in_schema=False)
async def signup_redirect(request: Request):
    # Determine the target URL. 
    # Since we are inside /api/v1 via main.py, and this router is included in main.py,
    # we can construct the redirect URL manually to be safe.
    # Logic: Redirect to the sibling path "register" under the same prefix.
    return RedirectResponse(url="/api/v1/auth/register", status_code=307)

# 3. Users Router - /api/v1/users (Provides /users/me, /users/{id})
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Manual Routers
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
# users router is likely handled by distinct settings route or combined above, checking conflicts.
# The previous line 48 had: api_router.include_router(user_settings.router, prefix="/users", tags=["users"])
# This conflicts with fastapi_users prefix. We need to decide. 
# Usually specific routes like /users/settings should be added to the fastapi_users router or have a different prefix.
# For Refactoring, I will enable user_settings but check its prefix path in next step.
api_router.include_router(user_settings.router, prefix="/users", tags=["users"]) 
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
