# Handovers: To Backend Developer

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- 현재 `Position` 모델은 사용자가 직접 수량과 평단가를 입력하는 방식입니다.
- 사용자의 요청에 따라, **Transaction(매수/매도)을 기록하면 Position(보유량, 평단가)이 자동으로 계산되는 방식**으로 리팩토링해야 합니다.
- `Transaction` 모델은 이미 정의되어 있으나(`models/transaction.py`), 로직이 구현되지 않았습니다.

## 해야 할 일 (Tasks)
1. **Transaction API 및 Service 구현**
   - `models/transaction.py`를 활용하여 `POST /api/v1/transactions` 엔드포인트 구현.
   - Request Body: `asset_id`, `type` (BUY, SELL), `quantity`, `price`, `timestamp`.

2. **Position 자동 계산 로직 (Event Sourcing Lite)**
   - 트랜잭션 발생 시 해당 User+Asset의 Position을 찾아 업데이트하는 로직 구현.
   - **매수(BUY) 시**:
     - 기존 포지션이 없으면 -> 새로 생성 (`quantity`, `buy_price` 초기화).
     - 기존 포지션이 있으면 -> **이동평균법(Weighted Average)** 으로 평단가 갱신.
       - `New_Avg = ((Old_Qty * Old_Avg) + (New_Qty * New_Price)) / (Old_Qty + New_Qty)`
       - `New_Qty = Old_Qty + New_Qty`
   - **매도(SELL) 시**:
     - 보유 수량(`quantity`) 감소.
     - 평단가(`buy_price`)는 변하지 않음.
     - `updated_at` 갱신.
     - (예외처리) 보유 수량보다 많은 매도 시 `400 Bad Request`.
     - 전량 매도 시 Position 삭제(또는 quantity=0 유지) 정책 결정 (일단 quantity=0 유지가 나음).

3. **기존 데이터 마이그레이션 (Optional)**
   - 기존 `Position` 데이터를 기반으로 초기 `BUY` Transaction을 하나씩 생성해주는 마이그레이션 스크립트(`scripts/migrate_positions_to_transactions.py`) 작성 권장.

## 기대 산출물 (Expected Outputs)
- `Transaction` 생성 시 `Position` 테이블의 값이 자동으로 변하는지 테스트 (`tests/test_transaction.py`).
- API 문서(`docs`)에 Transaction 엔드포인트 추가.
