# QA Report: E2E Flow Test v1.0.0

- **Date**: 2026-01-01
- **Tester**: QA Agent
- **Environment**: Local (Mac OS, Chrome)
- **Status**: 🔴 **FAIL** (Blocking Issue Found)

## 1. Summary
Manual E2E testing of the full user flow (Signup -> Login -> Asset Management) revealed a **critical blocking issue** in the Registration process. The frontend is attempting to call a non-existent API endpoint, preventing new users from signing up. Other authenticated features (Dashboard, Asset Management) work correctly when tested with an existing admin account.

## 2. Test Results

| TC ID | Scenario | Result | Notes |
|-------|----------|--------|-------|
| TC-E2E-01 | Main Page Redirect | ✅ PASS | Redirects to `/login` correctly. |
| TC-E2E-02 | Signup Page Navigation | ✅ PASS | "Sign up" link works. |
| TC-E2E-03 | **User Registration** | ❌ **FAIL** | **404 Not Found**. API Endpoint Mismatch. |
| TC-E2E-04 | Login (New User) | ❌ FAIL | Blocked by TC-E2E-03. |
| TC-E2E-05 | Dashboard Access | ✅ PASS | Verified with existing User 1 (Admin). |
| TC-E2E-06 | Asset Addition | ✅ PASS | Added 'AAPL' (10 qty @ $150). |
| TC-E2E-07 | Asset Verification | ✅ PASS | 'AAPL' appears in Dashboard/Positions. |

## 3. Defect Details

### [CRITICAL] Registration API Mismatch
- **Description**: The Frontend attempts to `POST` to `/api/v1/auth/signup`, but the Backend is configured to listen at `/api/v1/auth/register` (Standard `fastapi-users` route).
- **Evidence**:
  - Frontend Request: `POST http://localhost:5173/api/v1/auth/signup` -> Proxy -> `http://localhost:8000/api/v1/auth/signup` -> **404 Not Found**
  - Backend Configuration (`api.py`): `prefix="/auth"` with `fastapi_users.get_register_router(...)`.
- **Recommendation**: Update Frontend API client (`api.ts` or similar) to use `/register` instead of `/signup`.

### Screenshots
1. **Registration Error**:
   ![Registration 404](/Users/shin/.gemini/antigravity/brain/854a98a5-8df6-4390-9cad-9ec72ffe5f1f/registration_failure_error_1767257476283.png)

2. **Successful Asset Addition (Workaround)**:
   ![Asset Added](/Users/shin/.gemini/antigravity/brain/854a98a5-8df6-4390-9cad-9ec72ffe5f1f/final_positions_list_1767257432254.png)

## 4. Conclusion
The v1.0.0 release candidate is **NOT READY** due to broken user registration. This must be fixed in the Frontend before release.
