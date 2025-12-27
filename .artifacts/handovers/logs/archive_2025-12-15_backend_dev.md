# Handovers: To Backend Developer

## 날짜
2025-12-14

## 현재 상황 (Context)
- **v0.5.0 Released**: Transactions & Portfolio History complete.
- **v0.6.0 Planning Approved**: Focus on External Market Data integration (yfinance) and Analytics.
- **Reference**: `.artifacts/v0.6.0_implementation_plan.md` (See Backend Section).

## 해야 할 일 (Tasks)
- **Implement Market Data Service** (`src/engine/price_service.py`):
  - [x] Add `search_symbol(query: str) -> List[Dict]` using `yfinance`.
  - [x] Add `validate_symbol(symbol: str) -> bool`.
- **Create Market Routes** (`src/routes/market.py`):
  - [x] `GET /api/v1/market/search?q=...`: Returns search results.
  - [x] `GET /api/v1/market/validate?symbol=...`: Returns validation result.
- **Refinement**:
  - [x] (Optional) Update `Asset` creation to auto-fill Name/Category from `yfinance` info if available.

## 기대 산출물 (Expected Outputs)
- Functional `/market` endpoints.
- Updated `PriceService` with search capabilities.
