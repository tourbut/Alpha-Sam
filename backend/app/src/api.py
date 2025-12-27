from fastapi import APIRouter
from app.src.routes import assets, prices, positions, auth, users, portfolio, transactions, market, user_settings

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(user_settings.router, prefix="/users", tags=["users"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
