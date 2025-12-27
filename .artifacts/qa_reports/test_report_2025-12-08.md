# Test Report: Alpha-Sam Project
**Date:** 2025-12-08
**Tester:** QA Lead

## 1. Executive Summary
- **Backend**: Fully functionality. All Asset and Position APIs are working correctly, including complex aggregation logic (profit/loss).
- **Frontend**: Critical Issue. The Asset List page does not display any data.
- **Infrastructure**: Database requires migration `alembic upgrade head` which was not automatically applied in the dev environment.

## 2. Detailed Results

### 2.1 Backend API
| Feature | Scenario | Status | Notes |
|---------|----------|--------|-------|
| **Assets** | Create/List Assets | ✅ PASS | Returns correct data structure |
| **Positions** | Create Position | ✅ PASS | Successfully creates position and updates asset stats |
| **Pricing** | Refresh Prices | ✅ PASS | Updates `latest_price` |
| **Aggregation** | Calc Profit/Loss | ✅ PASS | `valuation`, `return_rate` calculated correctly to 2 decimal places |

### 2.2 Frontend UI
- **URL**: `http://localhost:5173/assets`
- **Status**: ❌ FAIL
- **Observation**: The table loads but remains empty. No data rows are rendered, even though the API returns a valid list of assets.
- **Root Cause (Hypothesis)**: Frontend component is not correctly mapping the API response, or there is a JavaScript error preventing rendering.

### 2.3 Environment
- Docker containers behave correctly.
- **Issue**: `alpha-sam-db` was missing the `positions` table on startup.
- **Fix**: Manually ran `alembic upgrade head`.

## 3. Bug Reports

### Bug #1: Asset List Not Displaying
- **Severity**: Critical
- **Description**: Users cannot see their assets on the dashboard.
- **Reproduction**:
  1. Ensure Backend has assets (verified via curl).
  2. Visit `/assets`.
  3. Observe empty table.

## 4. Recommendations
1. **Frontend Dev**: Fix the Asset List data binding.
2. **DevOps/Backend**: Ensure `alembic upgrade head` is run automatically in the `docker-compose` startup script or `entrypoint.sh` to prevent schema mismatch.
