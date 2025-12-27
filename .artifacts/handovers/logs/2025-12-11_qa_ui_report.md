# QA Report: UI/UX Improvements & Auth
**Date:** 2025-12-11
**Tester:** Antigravity (QA Persona)

## 1. Summary
- **Status:** **PASSED** ✅ (with Fix)
- **Environment:** Local Dev Server (:5174) + Backend (:8000)

## 2. Test Results

### 2.1 Auth Redirect
- **Scenario:** Access `/` without token.
- **Expected:** Redirect to `/login`.
- **Result:** **PASSED**. Redirect confirmed.

### 2.2 Login Flow
- **Scenario:** Enter credentials -> Sign In -> Redirect to Dashboard.
- **Initial Result:** **FAILED**. Frontend was calling `/api/v1/auth/token` (404).
- **Fix Applied:** Updated `api.ts` to use `/api/v1/auth/login`.
- **Final Result:** **PASSED**. Login successful, redirected to Dashboard.

### 2.3 Navbar Fixed Position
- **Scenario:** Scroll down on pages.
- **Verification:**
  - Code Review: `fixed w-full z-20 top-0` classes verified in `+layout.svelte`.
  - Browser Test: Navbar remains visible after login and navigation to `/assets`.
- **Result:** **PASSED**.

## 3. Issues Fixed
- **Bug:** Incorrect API endpoint in `api.ts` (`/auth/token` -> `/auth/login`).
- **DevOps:** Missing dependencies (`pyjwt`, `passlib`) and file sync issues in backend container. Resolved by rebuilding image.

## 4. Conclusion
UI improvements (Navbar, Padding) and Auth Redirects are fully functional.
Backend Auth API is verified healthy.
