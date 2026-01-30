# Handovers: To Backend Dev

## 날짜
- 2026-01-30

## 브랜치 (Version Control)
- `feature/backend-exchange-rate`

## 현재 상황 (Context)
- 환율 정보(USD/KRW)를 시스템 자산으로 관리하고 시세를 수집해야 합니다.
- `AdminAsset` 생성 시 System Portfolio에 자동으로 `Asset`을 생성하여 `PriceCollector`가 이를 수집하도록 만들어야 합니다.

## 해야 할 일 (Tasks)
1. **System Portfolio Service 구현 (`backend/app/src/services/system_portfolio_service.py`)**:
   - `get_or_create_system_user()`: 시스템 관리자 유저 확인/생성.
   - `get_or_create_system_portfolio()`: 시스템 포트폴리오 확인/생성.
   - `sync_admin_asset_to_system(admin_asset: AdminAsset)`: `AdminAsset`이 생성/수정될 때, 타입이 `EXCHANGE_RATE`(또는 `FOREX`)인 경우 System Portfolio에 해당 `Asset`을 생성/동기화하는 로직 구현.

2. **Admin API 수정 (`backend/app/src/routes/admin.py`)**:
   - `create_admin_asset` 엔드포인트에서 위 `sync_admin_asset_to_system`을 호출하도록 수정.

3. **데이터 마이그레이션/시딩**:
   - `AssetType` 관련 Enum이나 상수 정의에 `EXCHANGE_RATE` 추가.
   - (선택) 서버 시작 시 또는 별도 스크립트로 `USD/KRW` (Symbol: `KRW=X`) AdminAsset을 자동 생성.

4. **Price Collector 확인**:
   - `price_collector.py`가 `KRW=X` 심볼을 Yahoo Finance에서 정상적으로 가져오는지 테스트 코드(`tests/test_price_service.py`)로 확인.

## 기대 산출물 (Expected Outputs)
- Admin API를 통해 `EXCHANGE_RATE` 타입의 `USD/KRW` 자산을 등록하면, `assets` 테이블의 System Portfolio에 해당 자산이 생성되어야 함.
- `update_daily_prices` 태스크 실행 시 `prices_day` 테이블에 환율 데이터가 적재되어야 함.

## 참고 자료 (References)
- `backend/app/src/services/portfolio_service.py`
- `backend/app/src/services/tasks/price_tasks.py`
