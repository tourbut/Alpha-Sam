# Test Plan: v0.5.0 (Portfolio Foundations & Insights)

**Version:** 0.5.0
**Date:** 2025-12-14
**Author:** QA Team

## 1. Introduction
This test plan covers the verification of **Transaction Management** and **Portfolio History** features introduced in v0.5.0.

## 2. New Features to Verify

### 2.1 Transaction Management
- **Description**: Users can manually record Buy/Sell transactions.
- **Backend**: `POST /api/v1/transactions`, `GET /api/v1/transactions`.
- **Frontend**: `/transactions` page with Add Form and History List.

### 2.2 Portfolio History (Snapshots)
- **Description**: Tracking portfolio value over time to render history charts.
- **Backend**: Logic to create `PortfolioHistory` records (e.g., on price refresh).
- **Frontend**: "Portfolio History" Line Chart on Dashboard.

## 3. Test Scenarios

### 3.1 Backend API Tests

#### TC-TRX-01: Create Transaction (Buy)
- **Pre-condition**: Asset "AAPL" exists.
- **Action**: `POST /transactions` { asset_id, type="BUY", qty=10, price=150.0, date="2025-01-01" }.
- **Expected**:
  - Response 201 Created.
  - Portfolio Summary: 'AAPL' quantity increases by 10.
  - Portfolio Summary: Total Cost increases by $1500.

#### TC-TRX-02: Create Transaction (Sell)
- **Pre-condition**: Own 10 "AAPL".
- **Action**: `POST /transactions` { type="SELL", qty=5, price=160.0 }.
- **Expected**:
  - Response 201 Created.
  - Portfolio Summary: 'AAPL' quantity decreases to 5.
  - Portfolio Summary: Realized P/L calculated (Logic dependent).

#### TC-TRX-03: Input Validation
- **Actions**:
  - Qty = -1.
  - Price = 0.
  - Invalid Asset ID.
- **Expected**: 400 Bad Request or 404 Not Found.

#### TC-HIS-01: History Snapshot Trigger
- **Action**: Call `POST /prices/refresh` (or specific snapshot endpoint).
- **Expected**:
  - New record in `portfolio_histories` table with current timestamp and user's total equity.
  - `GET /portfolio/history` returns the new data point.

### 3.2 Frontend UI Tests

#### TC-UI-TRX-01: Add Transaction Form
- **Action**: Navigate to `/transactions`. Click "Add Transaction". Fill form. Submit.
- **Expected**: Form closes. Toast message "Transaction Added". New row appears in the list.

#### TC-UI-DASH-01: History Chart
- **Action**: Navigate to Dashboard.
- **Expected**: "Portfolio Value History" chart renders (not empty/error).
- **Edge Case**: If no history exists, chart should show "No Data" or empty state gracefully.

## 4. Test Data Strategy
- Use `check_v050_requirements.py` (to be created) for API automation.
- Use `browser_subagent` for UI Flow verification.

## 5. Exit Criteria
- All P0 scenarios (Buy/Sell, Chart Render) Pass.
- No regression in existing v0.4.0 features (Asset CRUD, Login).
