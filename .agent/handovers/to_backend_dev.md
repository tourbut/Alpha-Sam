# Handovers: To Backend Dev

## 날짜
- 2026-01-29

## 브랜치 (Version Control)
- `feature/implement-priceday-model`

## 현재 상황 (Context)
- 시세 데이터 관리 정책이 변경되었습니다.
- 기존의 단순 `Price` (timestamp, value) 테이블은 제거하고, **yfinance의 일봉(Daily Candle) 데이터를 저장하는 `PriceDay` 테이블**로 대체합니다.
- 실시간 현재가는 Redis를 통해 관리(기존 계획 유지)하되, 과거 이력 분석을 위해 DB에는 일별 OHLCV 데이터를 적재해야 합니다.

## 해야 할 일 (Tasks)
1. **모델 교체**:
   - `backend/app/src/models/price.py`를 수정하여 `Price` 클래스를 `PriceDay`로 변경하세요.
   - 테이블명: `prices_day`
   - 컬럼 구성 (yfinance 데이터 형태 준수):
     - `id`: UUID (PK)
     - `asset_id`: UUID (FK -> Asset)
     - `date`: Date (일봉 기준일)
     - `open`: Numeric (시가)
     - `high`: Numeric (고가)
     - `low`: Numeric (저가)
     - `close`: Numeric (종가)
     - `volume`: BigInteger (거래량)
     - `adjusted_close`: Numeric (수정 종가, Optional)
   - 복합 Unique Constraint: `(asset_id, date)`

2. **모델 참조 수정**:
   - `Asset` 모델(`backend/app/src/models/asset.py`)의 `prices` 관계를 `price_days` (또는 `daily_prices`)로 변경하고 `PriceDay`와 연결하세요.
   - 기타 코드에서 `Price` 모델을 참조하던 부분을 정리하세요.

3. **데이터 수집 로직 구현**:
   - `PriceService`에 특정 자산의 일별 시세를 yfinance에서 가져와 `PriceDay` 테이블에 저장/업데이트하는 메서드(`sync_daily_prices`)를 추가하세요.
   - `backend/app/src/services/tasks/price_tasks.py`에 하루 1회(예: 장 마감 후 또는 자정) 실행되는 Celery Task `update_daily_prices`를 추가하세요.

4. **API 수정**:
   - 시세 관련 API가 있다면 `PriceDay`를 조회하도록 수정하거나, 실시간 시세는 Redis를 계속 사용하도록 유지하세요.

5. **마이그레이션**:
   - `Price` 테이블 삭제 및 `PriceDay` 테이블 생성을 위한 Alembic 마이그레이션을 생성하고 실행하세요.

## 기대 산출물 (Expected Outputs)
- `PriceDay` 모델 및 `prices_day` 테이블 생성.
- `Price` 테이블 삭제.
- yfinance로부터 일봉 데이터를 수집하여 DB에 적재하는 기능 구현.

## 참고 자료 (References)
- yfinance data format: Date, Open, High, Low, Close, Volume
