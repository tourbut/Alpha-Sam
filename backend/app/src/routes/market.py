from fastapi import APIRouter, HTTPException, Query
from app.src.engine.price_service import price_service

router = APIRouter()

@router.get("/search")
async def search_symbol(q: str = Query(..., min_length=1, description="Symbol to search for (e.g. 'Apple')")):
    """
    Search for symbols using external market data provider (Yahoo Finance)
    """
    results = await price_service.search_symbol(q)
    return results

@router.get("/validate")
async def validate_symbol(symbol: str = Query(..., description="Symbol to validate (e.g. 'AAPL')")):
    """
    Validate if a symbol exists and we can get pricing for it.
    """
    is_valid = await price_service.validate_symbol(symbol)
    return {"symbol": symbol, "valid": is_valid}
