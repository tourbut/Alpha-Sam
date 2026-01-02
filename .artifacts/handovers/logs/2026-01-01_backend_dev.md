
# [Archived] Handovers: To Backend Developer (2026-01-01)

## 현재 상황 (Context)
- Frontend 및 QA 팀에서 전체 흐름(회원가입~자산등록) 점검 중.
- QA E2E Test에서 `/auth/signup` 404 에러로 Block됨.

## 완료된 작업 (Completed Tasks)
1. **Fix Registration Route Mismatch**:
   - `api.py`에 `POST /auth/signup` -> `POST /auth/register` (307 Redirect) 추가.
   - `curl` 테스트로 정상 회원가입 확인 (307 -> 201 Created).
   - 커밋: `fix(auth): add redirect alias for signup route` (on `feature/auth-redirect`).

---

## [Added 2026-01-01 18:40] v1.0.0 Handover (Position Fix)
### 현재 상황 (Context)
- QA E2E Test에서 자산 중복 추가 시 500 에러 발생.

### 완료된 작업 (Completed Tasks)
1. **Fix Position 500 Error**:
   - `positions.py`에서 `IntegrityError` 처리 로직 추가.
   - 중복 포지션 생성 시 400 Bad Request 반환 (`Position for this asset already exists.`).
   - 커밋: `fix(api): handle integrity error for duplicate positions` (on `bugfix/position-500-error`).

## 다음 단계
- QA 팀에게 500 에러 해결 확인 요청 (이젠 400 에러가 나와야 정상).
