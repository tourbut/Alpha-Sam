# Handovers: To Backend Developer

## 날짜
2025-12-09

## 현재 상황 (Context)
- 사용자 회원가입 및 로그인을 위한 인증 시스템(Authentication)이 필요합니다.
- 기존 자산 관리 기능에 사용자 개념을 도입하기 위한 첫 단계입니다.

## 해야 할 일 (Tasks)
1. **User 모델 및 스키마 구현**:
   - `app/models/user.py`: `User` SQLModel (id, email, password_hash, is_active 등).
   - Alembic 마이그레이션 생성 및 적용 (`alembic revision --autogenerate`).
2. **보안 유틸리티 구현**:
   - `app/core/security.py`: 비밀번호 해싱(bcrypt), JWT 토큰 생성/검증 함수.
3. **Auth API 구현**:
   - `app/api/endpoints/auth.py`:
     - `POST /auth/signup`: 회원가입 (이메일 중복 체크).
     - `POST /auth/login`: 로그인 (Access Token 반환).
     - `GET /auth/me`: 현재 로그인한 사용자 정보 조회 (Dependency Injection 활용).
4. **Router 등록**:
   - `app/api/api.py`에 auth 라우터 추가.

## 기대 산출물 (Expected Outputs)
- Swagger UI에서 회원가입 및 로그인을 성공하고, JWT 토큰을 발급받을 수 있어야 함.

## 참고 자료 (References)
- FastAPI Security Docs: https://fastapi.tiangolo.com/tutorial/security/
