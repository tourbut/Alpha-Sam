# QA Report & v0.3.0 Test Plan
**Date:** 2025-12-12
**Author:** QA Agent

## 1. Regression Test Report (Refactoring Verification)

**Subject:** Verification of Backend Structure Refactoring (`app/src`, CRUD extraction).

### Findings
During the initial regression checking, **Critical Blockers** were identified that prevented the backend from starting.

#### 🔴 Critical Issue 1: Missing Schema Definition
- **Description**: `ImportError: cannot import name 'Token' from 'app.src.schemas.user'`.
- **Cause**: The `Token` Pydantic model was missing from `backend/src/schemas/user.py`, likely lost during file moves.
- **Resolution**: **[QA Hotfix]** Added `Token` class to `user.py`.

#### 🔴 Critical Issue 2: Circular Import Dependency
- **Description**: `ImportError: cannot import name 'deps' from partially initialized module ...`.
- **Cause**: `backend/src/routes/users.py` imported `deps` from `app.src.api`, while `api.py` imports `users.py`.
- **Resolution**: **[QA Hotfix]** Changed import in `users.py` to `from app.src import deps`.

### Verification Status
- **Backend Startup**: ✅ Success (after hotfixes).
- **Functionality Check**:
  - **Signup**: ✅ Verified (User creation via API).
  - **Login**: ✅ Verified (Token issuance).
  - **Asset Creation**: ✅ Verified (DB insertion).
  - **Asset List**: ✅ Verified (Retrieval).

> **Note to Dev**: Please review the hotfixes applied directly to the codebase to ensuring they align with architectural standards.

---

## 2. v0.3.0 Test Plan: User Settings

**Objective:** Verify the new "User Settings" page and functionality.
**References:** `user_settings_design.md`

### Test Scenarios

#### TC-SET-01: Page Access & Protection
- **Pre-condition**: User is NOT logged in.
- **Action**: Access `/settings` directly in browser URL.
- **Expected**: Redirect to `/login` (or Home).
- **Action**: Log in and access `/settings`.
- **Expected**: Settings page renders with "Profile" and "Security" cards.

#### TC-SET-02: Update Profile (Nickname)
- **Action**: Enter a new valid nickname (e.g., "AlphaTrader") and click Save.
- **Expected**: Toast/Notification "Profile Updated". Navbar/Header updates to show new nickname immediately.
- **Verification**: Reload page, nickname persists. Check `GET /users/me` response.

#### TC-SET-03: Password Change Validation
- **Case A (Wrong Current)**: Enter incorrect current password. -> Expect Error message (400).
- **Case B (Mismatch New)**: Enter "NewPass1!" and Confirm "NewPass2!". -> Expect UI Validation Error (Frontend interception preferred).
- **Case C (Same as Old)**: New password == Old password. -> Expect Error (Backend 400).

#### TC-SET-04: Password Change Success
- **Action**: Correctly change password.
- **Expected**: Success message.
- **Verification**: Logout. Attempt login with OLD password (Fail). Attempt login with NEW password (Success).

---

## 3. v0.3.0 Test Plan: Price API

**Objective:** Verify integration of Real-time Price Data via `yfinance`.
**References:** `price_api_analysis.md`

### Test Scenarios

#### TC-PRC-01: Real Data Accuracy
- **Action**: Add Assets: "AAPL" (Stock), "BTC-USD" (Crypto).
- **Action**: View Dashboard.
- **Expected**: Prices displayed are non-zero and match roughly with `finance.yahoo.com` (within minute-delay variance).
- **Validation**: Compare System Price vs Public Source.

#### TC-PRC-02: Symbol Mapping Handling
- **Action**: Add Asset "BTC" (without -USD).
- **Expected**: System logic (Service layer) maps it to `BTC-USD` for query, or returns valid price.
- **Note**: Check if logic handles common missing suffixes for Crypto if detailed in design.

#### TC-PRC-03: Server-side Caching
- **Action**: Load Dashboard (API Call triggered). Record response time.
- **Action**: Refresh 5 times within 10 seconds.
- **Expected**: 1st call ~1-2s (External Fetch). Subsequent calls < 200ms (Redis/Memory Cache hit).
- **Log**: Check Backend logs for "Cache Hit" vs "Fetching from yfinance".

#### TC-PRC-04: Non-Blocking Behavior
- **Concerns**: `yfinance` is synchronous.
- **Test**: Trigger Price Refresh while simultaneously trying to navigate UI or call other lightweight APIs.
- **Expected**: Backend should not freeze; other requests should be served via async event loop (requires `run_in_executor`).
