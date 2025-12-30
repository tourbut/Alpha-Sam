# [2025-12-28] Backend Auth Implementation

## Context
Refactored authentication system using `fastapi-users`.

## Tasks Completed
- [x] Create branch `feature/backend-auth-research`
- [x] Research and test dependencies
- [x] Analyze User model compatibility
- [x] Audit X-User-Id usage
- [x] Implement `fastapi-users` (Auth Backend, UserManager, Router)
- [x] Refactor `deps.get_current_user` to support X-User-Id fallback

## Changes
- `pyproject.toml`: Added `fastapi-users[sqlalchemy]`.
- `src/models/user.py`: Inherit `SQLAlchemyBaseUserTable`.
- `src/core/users.py`, `src/core/auth.py`: New files.
- `src/deps.py`: Refactored.
- `main.py`: Registered routers.

## Note
- Verification tests failed due to DB connection refusal. Please ensure Postgres is running (`docker-compose up -d db`).
