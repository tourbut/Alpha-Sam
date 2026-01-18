# QA Report: Regression Test v1.0.0

## Test Metadata
- **Date**: 2026-01-04
- **Environment**: Local (Mac OS, zsh)
- **Testers**: QA Agent
- **Scope**: Full System Regression (Auth, Dashboard, Assets)

## Test Summary
| Scenario | Status | Key Issues |
| :--- | :---: | :--- |
| **Auth** (Signup/Login) | **PASS** | Auto-login works, redirect works. |
| **Dashboard** (Load/Chart) | **PASS (Fixed)** | Data Leak Resolved. New users see only global assets (owner_id: None). |
| **Assets** (CRUD) | **PASS (Fixed)** | Asset Creation now works (201 Created). |

## Detailed Results

### 1. Authentication (Auth)
- **TC-REG-01**: Signup with new user -> Auto Login.
    - Result: **PASS**
    - Notes: Signup `qa_regression_test@example.com` successful. Redirected to Dashboard.

### 2. Dashboard
- **TC-REG-02**: Check Portfolio Cards (Assets, Valuation).
    - Result: **PASS (Re-verified)**
    - Notes:
        - **Initial Fail**: "Total Assets" showed 13.
        - **Fix Verification**: 
            - Removed `X-User-Id` dependency injection override.
            - New user now sees only 2 Global Assets (Legacy test assets).
            - Private assets of other users are NOT visible.

- **TC-REG-03**: Verify Allocation Chart Rendering.
    - Result: **PASS**
    - Notes: Chart renders correctly with user's own data (or empty).

### 3. Asset Management
- **TC-REG-04**: Add New Asset (TSLA).
    - Result: **PASS (Re-verified)**
    - Notes:
        - **Initial Fail**: 500 Internal Server Error.
        - **Fix Verification**: 
            - Fixed `TypeError` in `AssetService` (missing keyword arguments in `crud_asset` calls).
            - Creation of `AAPL` returned **201 Created**.
            - Asset persisted in database.
        
- **TC-REG-05**: Asset Listing Update.
    - Result: **PASS**
    - Notes: Asset list updates correctly after creation.

- **TC-REG-06**: Add Position to Existing Asset (AAPL).
    - Result: **PASS**
    - Notes: Verified adding position to newly created asset works.

## Overall Verdict
**[PASSED]**
v1.0.1 (Hotfix) is **READY** for release.
Critical bugs in User Data Isolation and Asset Creation have been resolved and verified.
