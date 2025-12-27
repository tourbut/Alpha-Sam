# Handovers: To Backend Developer

## 날짜
2025-12-27

## 브랜치 (Version Control)
- `feature/backend-auth-research`

## 현재 상황 (Context)
- v0.7.0 완료 후 v0.8.0(Authentication) 작업 준비 단계입니다.
- `FastAPI Users` 라이브러리를 도입하여 표준 인증 시스템을 구축할 예정입니다.

## 해야 할 일 (Tasks)
1. `feature/backend-auth-research` 브랜치 생성.
2. `fastapi-users[sqlalchemy]` 등 필요한 라이브러리 조사 및 `pyproject.toml` 의존성 추가 테스트 (로컬).
3. 현재 `User` 모델(`src/models/user.py`)과 `fastapi-users`의 기본 모델 간 호환성 분석.
   - 어떤 필드가 추가/변경되어야 하는지 파악.
4. 프로젝트 전반에서 `X-User-Id` 헤더를 사용하는 위치를 모두 찾아 리스트업 (`grep` 활용).
   - 향후 `current_user` 의존성 주입으로 대체하기 위함.

## 기대 산출물 (Expected Outputs)
- `X-User-Id` 사용처 리스트 (markdown 파일 또는 이슈 코멘트).
- `pyproject.toml`에 추가될 의존성 목록.
- `User` 모델 변경사항 분석 리포트 (간단한 메모).

## 참고 자료 (References)
- [FastAPI Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- `src/api/deps.py` (현재 유저 식별 로직)
