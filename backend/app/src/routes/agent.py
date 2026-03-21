from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.src.core import security
from app.src.models.user import User
from app.src.schemas.user import UserRead, Token
from app.src.crud import users as crud_user
from app.src.deps import SessionDep_async

router = APIRouter()

# 1. 하드코딩된 에이전트 필수 API 명세 정의
AGENT_API_DOCS = [
    {
        "method": "GET",
        "url": "/api/v1/portfolios",
        "description": "Get all portfolios for the authenticated user."
    },
    {
        "method": "POST",
        "url": "/api/v1/portfolios",
        "description": "Create a new portfolio.",
        "body": {
            "name": "string",
            "description": "string (optional)",
            "currency": "string (default: USD)"
        }
    },
    {
        "method": "GET",
        "url": "/api/v1/portfolios/{portfolio_id}",
        "description": "Get a specific portfolio by ID."
    },
    {
        "method": "DELETE",
        "url": "/api/v1/portfolios/{portfolio_id}",
        "description": "Delete a specific portfolio by ID."
    },
    {
        "method": "POST",
        "url": "/api/v1/assets",
        "description": "Create a new asset and link to portfolio.",
        "body": {
            "portfolio_id": "string (UUID v4)",
            "symbol": "string (e.g. AAPL)",
            "name": "string",
            "category": "string (Crypto, Stock, etc.)"
        }
    },
    {
        "method": "GET",
        "url": "/api/v1/portfolios/{portfolio_id}/positions",
        "description": "Get all current positions for a portfolio."
    },
    {
        "method": "POST",
        "url": "/api/v1/transactions",
        "description": "Record a buy/sell transaction.",
        "body": {
            "portfolio_id": "string (UUID v4)",
            "asset_id": "string (UUID v4)",
            "type": "string (BUY or SELL)",
            "quantity": "float",
            "price": "float",
            "executed_at": "string (ISO 8601 datetime)"
        }
    }
]

@router.post("/login", response_model=Any)
async def login_agent(*, 
    session: SessionDep_async,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 Token Login optimized for Agents.
    Returns access_token and plain API specifications required for Agentic control.
    """
    user = await crud_user.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    access_token = security.create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "api_docs": AGENT_API_DOCS
    }

@router.get("/docs", response_model=Any)
async def get_agent_docs() -> Any:
    """
    Get the API specifications for Agents.
    """
    return AGENT_API_DOCS
