# Handovers: To Backend Developer

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- 로그인 시 `column users.is_public_leaderboard does not exist` 에러가 발생하여 서비스 이용이 불가능합니다.
- 최근 모델에 추가된 `is_public_leaderboard` 컬럼이 실제 DB에 반영되지 않은 것으로 보입니다.

## 해야 할 일 (Tasks)
1. **Alembic Migration 점검**:
   - `alembic/versions` 내에 `is_public_leaderboard` 컬럼을 생성하는 마이그레이션 파일이 있는지 확인.
   - 없다면 `alembic revision --autogenerate -m "add is_public_leaderboard to user"` 등을 통해 생성.
   - 있다면 `alembic upgrade head`를 통해 실제 DB에 반영.
2. **DB 스키마 확인**:
   - 실제 서버 기동 후 로그인 시 테스터 계정(`tester@example.com`)으로 로그인이 정상적으로 되는지 확인. `column not found` 에러가 더 이상 발생하지 않아야 함.

## 기대 산출물 (Expected Outputs)
- `is_public_leaderboard` 컬럼이 추가된 Alembic 마이그레이션 파일.
- `alembic upgrade head`가 완료되어 로그인이 정상 동작하는 상태.

## 참고 자료 (References)
- `.artifacts/projects/v1.1.0_architecture_draft.md`
- `backend/app/src/models/user.py`

# 2차 작업 (Auth Router Fix & Stabilization)

## 날짜
- 2026-01-10 14:10

## 작업 내역 (Tasks Completed)
1. **인증 라우터 정리 (backend/app/src/api.py)**:
   - fastapi_users의 Auth 및 Register 라우터를 주석 처리하여 커스텀 auth 라우터와의 중복을 제거함.
   - 현재 활성화된 경로:
     - POST /api/v1/auth/login (Custom)
     - POST /api/v1/auth/signup (Custom)
2. **DB 스키마 및 마이그레이션 확인**:
   - alembic upgrade head 실행 완료.
   - User 모델의 is_public_leaderboard 컬럼 존재 확인.
3. **검증 (Verification)**:
   - curl 테스트를 통해 /api/v1/auth/login 엔드포인트 정상 동작 확인 (200 OK, Token 반환).
   - tester@example.com 계정으로 로그인 성공 -> SQL 에러(Column not found) 없음 확인.

## 결과
- 백엔드 API 엔드포인트가 프론트엔드의 기대(functional_inventory.md)와 일치하도록 정리됨.
- 로그인 오류 해결됨.
