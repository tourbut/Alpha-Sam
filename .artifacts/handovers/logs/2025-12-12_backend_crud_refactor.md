# Handovers: To Backend Developer

## 2025-12-12

## 현재 상황 (Context)
- 현재 `backend/app/src/routes/*.py` 파일들 내부에 데이터베이스 접근 로직(SQLAlchemy 쿼리)이 직접 포함되어 있습니다.
- 코드의 유지보수성과 재사용성 향상, 그리고 관심사의 분리를 위해 DB 접근 로직을 CRUD 레이어로 추출해야 합니다.

## 해야 할 일 (Tasks)
1. `backend/app/src/crud/` 디렉토리가 없다면 생성하고 `__init__.py` 포함하기.
2. `backend/app/src/crud/crud_asset.py` 구현:
   - `create_asset(session, obj_in)`
   - `get_assets(session, skip, limit)` (Price, Position 조인 로직 포함 여부 결정)
   - `remove_asset(session, asset_id)`
3. `backend/app/src/crud/crud_user.py` 구현:
   - `get_user_by_email(session, email)`
   - `create_user(session, obj_in)`
   - `update_user(session, db_user, obj_in)`
   - `authenticate(session, email, password)` (선택사항, core/security에 있을 수도 있음)
4. `backend/app/src/routes/assets.py` 리팩토링:
   - 라우터 핸들러 내의 SQL 쿼리를 제거하고 `crud_asset` 모듈의 함수를 호출하도록 변경.
5. `backend/app/src/routes/auth.py`, `backend/app/src/routes/users.py` 리팩토링:
   - 직접적인 DB 호출을 `crud_user` 모듈의 함수로 대체.
6. (선택) `backend/app/src/routes/positions.py` 도 동일한 패턴으로 리팩토링 (`crud_position.py` 필요 시 생성).

## 기대 산출물 (Expected Outputs)
- `backend/app/src/crud/` 패키지 구성.
- `routes` 코드가 간결해지고 비즈니스 로직 요청만 남음.
- 기능 동작은 기존과 동일해야 함 (회귀 테스트 필요).

## 참고 자료 (References)
- 현재 `backend/app/src/routes/` 내의 코드들.
- FastAPI 프로젝트 구조 일반적인 모범 사례 (CRUD 패턴).


## Execution Result (2025-12-12 Part 3)
- Introduced CRUD layer ().
- Refactored , ,  to use CRUD layer.
- Improved code reusability and separation of concerns.


## Execution Result (2025-12-12 Part 3)
- Introduced CRUD layer (app.src.crud).
- Refactored routes/assets.py, auth.py, users.py to use CRUD layer.
- Improved code reusability and separation of concerns.
