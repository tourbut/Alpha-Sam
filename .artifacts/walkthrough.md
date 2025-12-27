# Walkthrough - Alpha-Sam v0.5.0

**Goal**: Verify Portfolio Foundations & Insights (Transactions & History).

## Changes
- **Backend**:
  - Added `Transaction` and `PortfolioHistory` models.
  - Implemented `/api/v1/transactions` (CRUD).
  - Implemented `/api/v1/portfolio/history` and `/snapshot`.
  - Atomic position updates on Transaction creation.
- **Frontend**:
  - New Page: `/transactions` (List & Add Transaction).
  - Dashboard: Added "Portfolio Value History" chart.
  - API Client: Updated to support new endpoints.

## Verification Steps

### 1. Transaction Management
1.  Navigate to **/transactions**.
2.  Click **"Add Transaction"**.
3.  Select an Asset, choose **BUY**, enter Quantity and Price.
4.  Submit.
5.  Verify the transaction appears in the list.
6.  Navigate to **/positions** (or Dashboard) to verify the Position quantity increased.

### 2. Portfolio History
1.  (Optional) Trigger a snapshot via API or wait for automated process (currently manual via script or new button if added, but for now use the script `check_v050_features.py` which triggers it, or just rely on manual DB entry if you know how). *Note: We added `createPortfolioSnapshot` to API but didn't add a button in UI yet. You can run `python3 check_v050_features.py` to generate some history data.*
2.  Navigate to **Dashboard**.
3.  Check the **"Performance (Value)"** chart.
4.  It should display the trend of your portfolio value over time.

## Automated Verification
Run the verification script to test the backend logic:
```zsh
python3 check_v050_features.py
```
Output should end with `✅ v0.5.0 Features Verified`.
