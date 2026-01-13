# QA Test Report: v1.2.0 & Dashboard Fix

**Date**: 2026-01-11
**Tester**: QA Engineer (Agent)
**Scope**: Dashboard Loading Bug, v1.2.0 Portfolio/Transaction Features

## Summary
The critical dashboard loading bug has been resolved. The new v1.2.0 features (Multi-Portfolio, Transaction-based Positions) are functioning correctly on the backend API level. A schema mismatch causing 500 errors on the Position API was identified and fixed during testing.

## Test Results

| ID | Test Case | Status | Notes |
|----|-----------|--------|-------|
| TC-DASH-01 | Dashboard Loading (API) | **PASS** | `GET /api/v1/portfolios/` returns 200 OK. Double prefix issue resolved. |
| TC-PORT-01 | Create Portfolio | **PASS** | Successfully created "QA Test" portfolio. |
| TC-PORT-02 | List Portfolios | **PASS** | Returns list including default and new portfolios. |
| TC-TX-01 | Create Transaction (BUY) | **PASS** | BUY 10 units @ 100 correctly creates transaction. |
| TC-POS-01 | Position Calculation (BUY) | **PASS** | Position created with Qty 10, Avg 100. |
| TC-TX-02 | Create Transaction (SELL) | **PASS** | SELL 5 units @ 120 correctly creates transaction. |
| TC-POS-02 | Position Calculation (SELL) | **PASS** | Position updated to Qty 5, Avg 100 (Unchanged). |
| TC-API-01 | Position API Schema | **FIXED** | Fixed `PositionRead` schema to use `avg_price` instead of `buy_price` to prevent 500 Error. |

## Issues Found & Resolved
- **Issue**: `GET /api/v1/portfolios/{id}/positions` returned 500 Internal Server Error.
- **Root Cause**: `PositionRead` Pydantic schema was still expecting `buy_price` (old model), but `Position` model now uses `avg_price`.
- **Resolution**: Updated `backend/app/src/schemas/position.py` to match the model. Confirmed fix.

## Conclusion
The backend is stable and ready for release. Frontend functionality depends on these APIs, which are now verified. Manual UI verification is recommended as final check, but API logic is sound.
