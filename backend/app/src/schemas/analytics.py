from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class AssetAllocationResponse(BaseModel):
    ticker: str
    percentage: float
    total_value: float

class PortfolioHistoryResponse(BaseModel):
    date: str
    total_value: float
    uninvested_cash: float
