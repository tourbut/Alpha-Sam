# Handovers: To Backend Developer

## 날짜
2025-12-12

## 현재 상황 (Context)
- CRUD 리팩토링이 완료되어 코드가 `app/src` 구조로 안정화되었습니다.
- 이제 미뤄두었던 **v0.3.0** 핵심 기능 개발을 진행합니다.

## 해야 할 일 (Tasks)

1. **Feature: User Settings (닉네임 & 비밀번호)**
   - **참고**: `.artifacts/prompts/projects/alpha_sam/user_settings_design.md`
   - **Model**: `app/src/models/user.py`에 `nickname` 필드 추가.
   - **Migration**: `alembic revision --autogenerate`로 마이그레이션 생성 및 적용.
   - **API**:
     - `PUT /api/v1/users/me`: 닉네임 수정 구현 (CRUD 모듈 활용).
     - `POST /api/v1/users/password`: 비밀번호 변경 구현.

2. **Feature: Real-time Price API (yfinance)**
   - **참고**: `.artifacts/prompts/projects/alpha_sam/price_api_analysis.md`
   - **Service**: `app/src/services/price_service.py` (또는 해당하는 위치) 수정.
   - **Logic**: 
     - Mock 데이터를 제거하고 `yfinance` 라이브러리로 실제 가격 조회.
     - Redis Cache TTL(예: 60s) 적용하여 호출 횟수 제한.
     - `asyncio.to_thread` 등을 사용하여 동기 함수인 yfinance가 Event Loop를 차단하지 않도록 처리.

## 기대 산출물 (Expected Outputs)
- DB `users` 테이블에 `nickname` 컬럼 추가됨.
- `/users/me` 및 `/users/password` API가 정상 동작.
- 자산 시세 조회 시 실제 주식/코인 가격 반환.


## Execution Result (2025-12-12 Part 4)
- Implemented User Settings API using CRUD layer ().
- Updated  to use  for non-blocking yfinance calls.
- Verified migration status.


## Execution Result (2025-12-12 Part 4)
- Implemented User Settings API using CRUD layer (crud_user.update_user_password).
- Updated PriceService to use asyncio.to_thread for non-blocking yfinance calls.
- Verified migration status.
