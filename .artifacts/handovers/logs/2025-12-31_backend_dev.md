# Handovers to Backend Developer

## Current Context
- **Role**: Backend Developer
- **Phase**: v0.9.0 Implementation (Data Migration & Optimization)
- **Reference**: [.artifacts/projects/plans/v0.9.0_migration_plan.md](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.artifacts/projects/plans/v0.9.0_migration_plan.md)

## Tasks

### 1. Data Migration Script (Priority: High)
- **File**: `backend/scripts/migrate_v090_legacy_data.py`
- **Goal**: Clean up legacy positions with `owner_id IS NULL`.
- **Logic**:
  - Initialize async session.
  - Find all `Position` rows where `owner_id` is NULL.
  - Update them to `owner_id = 1` (Default Admin User).
  - Print summary of updated rows.
- **Note**: Ensure this script can be run idempotently (safe to re-run).

### 2. Portfolio Optimization (Priority: Medium)
- **File**: `backend/app/src/routes/portfolio.py`
- **Function**: `create_portfolio_snapshot`
- **Issue**: N+1 Query. Currently iterating validation in loop.
- **Fix**:
  - Use `IN` clause to fetch latest prices for all target assets in one query.
  - Map `asset_id` -> `price` in memory.
  - Calculate metrics using the map.

## Deliverables
- `migrate_v090_legacy_data.py`
- Optimized `portfolio.py`
- Verification: Run the script locally and confirm `create_portfolio_snapshot` works via Swagger.
# Handovers: To Backend Developer

## 날짜
2025-12-31

## 현재 상황 (Context)
- v0.9.0의 핵심인 데이터 마이그레이션과 성능 최적화를 진행해야 합니다.
- 포트폴리오 조회 시 N+1 쿼리 문제가 식별되었습니다.

## 해야 할 일 (Tasks)
1. **Migration Script 작성**:
   - `backend/scripts/migrate_v090_legacy_data.py` 작성.
   - `positions` 테이블에서 `owner_id IS NULL`인 레코드를 찾아 `Default Admin (ID: 1)`으로 업데이트.
   - 실행 결과(업데이트된 건수)를 출력하도록 구현.
2. **Portfolio API 최적화**:
   - `backend/app/src/routes/portfolio.py`의 `create_portfolio_snapshot` 함수 리팩토링.
   - 자산 현재가 조회 시 루프 내 쿼리 대신 `IN` 절을 사용하여 일괄 조회(Batch Fetch) 하도록 변경.
3. **검증**:
   - 로컬 환경에서 마이그레이션 스크립트 실행 테스트.
   - Swagger UI로 포트폴리오 스냅샷 생성 정상 동작 확인.

## 기대 산출물 (Expected Outputs)
- `migrate_v090_legacy_data.py`
- 최적화된 `portfolio.py`

## 참고 자료 (References)
- [.artifacts/handovers/to_backend_dev.md](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.artifacts/handovers/to_backend_dev.md) (Log)
