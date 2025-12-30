# Test Plan: v0.8.0 (Authentication System)

**Version:** 0.8.0
**Date:** 2025-12-28
**Author:** QA Team

## 1. Introduction
This test plan covers the verification of the **Authentication System** features introduced in v0.8.0. This includes User Registration, Login, Logout, and Token Management.

## 2. New Features to Verify

### 2.1 User Authentication
- **Description**: Secure user registration and login using JWT.
- **Backend**: `fastapi-users` integration, JWT strategy, `SQLModel` User adapter.
- **Frontend**: Login page, Signup page, Auth store (Pinia), Protected Routes.

## 3. Test Scenarios

### 3.1 Backend API Tests

#### TC-AUTH-01: User Registration
- **Action**: `POST /auth/register` { email, password, is_active=true }
- **Expected**:
  - Response 201 Created.
  - User created in DB with hashed password.
  - `is_active` is true.

#### TC-AUTH-02: User Registration - Duplicate Email
- **Pre-condition**: User with email "test@example.com" exists.
- **Action**: `POST /auth/register` { email="test@example.com", ... }
- **Expected**: 400 Bad Request (User already exists).

#### TC-AUTH-03: User Registration - Invalid Password
- **Action**: `POST /auth/register` { password="123" } (Assuming min length > 3)
- **Expected**: 400 Bad Request (Password does not meet requirements).

#### TC-AUTH-04: Login - Success
- **Action**: `POST /auth/jwt/login` { username, password }
- **Expected**:
  - Response 200 OK.
  - Body contains `access_token` and `token_type` "bearer".

#### TC-AUTH-05: Login - Invalid Credentials
- **Action**:
  - Wrong Password
  - Non-existent User
- **Expected**: 400 Bad Request or 401 Unauthorized.

#### TC-AUTH-06: Logout
- **Action**: `POST /auth/jwt/logout` (Header: Authorization: Bearer <token>)
- **Expected**:
  - Response 200/204.
  - Token is blacklisted/invalidated (if relying on stateful or just client removal). *Note*: Stateless JWTs might not be invalidated server-side unless a blacklist is implemented, but user session should be ended.

### 3.2 Frontend UI Tests

#### TC-UI-AUTH-01: Signup Flow
- **Action**: Navigate to `/register`. Fill form. Submit.
- **Expected**: Redirect to Login or Dashboard. Toast message "Registration Successful".

#### TC-UI-AUTH-02: Login Flow
- **Action**: Navigate to `/login`. Fill valid credentials. Submit.
- **Expected**: Redirect to Dashboard. Header shows "Logout" button instead of "Login".

#### TC-UI-AUTH-03: Protected Route Access
- **Action**: Navigate to `/dashboard` (or any protected route) without logging in (clear storage).
- **Expected**: Redirected to `/login`.

#### TC-UI-AUTH-04: Token Expiration (Simulation)
- **Action**: Manually modify/invalidate token in storage or wait for expiration. Refresh page.
- **Expected**: Redirected to `/login`.

## 4. Test Data Strategy
- Use `browser_subagent` for full e2e flows.
- Manual verification on staging environment if available.

## 5. Exit Criteria
- All P0 scenarios (Login/Signup/Protected Routes) Pass.
- No regression in existing features (Portfolio viewing while logged in).
