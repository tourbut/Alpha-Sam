# QA Report: Full Regression Test

**Date**: 2026-01-08
**Tester**: QA Agent
**Context**: Regression verification after Svelte 5 Runes refactor and Backend Auth redirect fix.

## Status: PASSED 🟢

All critical authentication and dashboard functionalities are working as expected.

## Test Summary

| Test Case | Scenario | Status | Notes |
|:---|:---|:---|:---|
| **TC-REG-01** | **Login Flow** | **PASS** | Successfully logged in with `tester@example.com`. Redirected to `/` without error. |
| **TC-REG-02** | **Dashboard Loading** | **PASS** | "Portfolio Dashboard" visible. Total Assets: 2. No loading/error states. |
| **TC-REG-03** | **Refresh Prices** | **PASS** | Button interactive, state updates (Refreshing -> Refresh Prices). |
| **TC-REG-04** | **Session Persistence** | **PASS** | Reloading page (F5) maintains login state on Dashboard. |
| **TC-REG-05** | **Remember ID (Save)** | **PASS** | Email pre-filled after checking box, logging in, and logging out. |
| **TC-REG-06** | **Remember ID (Clear)** | **PASS** | Email NOT pre-filled after unchecking box and re-logging. |
| **TC-REG-07** | **Logout** | **PASS** | Redirects to `/login` correctly. |

## Detailed Observations

- **Frontend/Backend Sync**: The previous 401/307 errors are resolved. API calls to `/api/v1/portfolio/summary/` return 200 OK.
- **Svelte 5 Runes**: No runtime errors observed. Reactivity (charts, counts) appears stable.

## Conclusion

The release candidate is stable for authentication and core portfolio viewing features.
