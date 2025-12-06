# Domain Rules – Alpha-Sam

## 핵심 도메인 개념

1. Asset (자산)
   - 사용자가 관리하는 개별 투자 대상.
   - 예: 특정 코인(예: BTC), 특정 주식(예: AAPL), ETF 등.

2. Position / Holding (보유 내역)
   - 특정 자산에 대한 사용자의 보유 상태.
   - 매수 단가, 수량, 매수 일자 등의 정보를 포함.

3. Price (시세)
   - 외부 데이터 소스에서 가져오는 현재 단가.
   - 시점별로 변동 가능.

4. Portfolio (포트폴리오)
   - 사용자가 보유한 모든 자산/포지션의 집합.
   - 전체 평가액, 전체 손익, 전체 수익률을 계산하는 단위.

## 주요 필드 규칙

### Asset

- 필수:
  - `symbol`: 문자열, 대문자 추천 (예: BTC, AAPL)
  - `name`: 사람 친화적인 이름 (예: Bitcoin, Apple Inc.)
- 선택:
  - `category`: 코인, 주식, ETF 등 카테고리
- 제약:
  - 동일 사용자의 동일 `symbol`은 중복 생성 불가(일반적으로 1개만 허용).

### Position / Holding

- 필수:
  - `asset_id`: Asset 참조
  - `quantity`: 보유 수량 (0 이상, 음수 불가)
  - `buy_price`: 매수 단가 (0 초과)
- 선택:
  - `buy_date`: 매수 일자
- 제약:
  - `quantity == 0`일 경우, 사실상 보유하지 않는 것으로 처리할 수 있으나, 과거 이력 보존이 필요하면 삭제 대신 상태 플래그를 둘 수 있음.

### Price

- 필수:
  - `asset_id` 또는 `symbol`
  - `value`: 현재 가격
  - `timestamp`: 시세 기준 시각
- 규칙:
  - 외부 API 장애로 값을 가져오지 못한 경우 `null` 또는 에러를 명확히 구분하여 처리해야 함.

## 수익 및 평가액 계산 규칙

### 단일 포지션 기준

- 평가액 (valuation)
  - `valuation = current_price * quantity`
- 손익 (profit_loss)
  - `profit_loss = (current_price - buy_price) * quantity`
- 수익률 (return_rate, %)
  - `return_rate = ((current_price - buy_price) / buy_price) * 100`

### 전체 포트폴리오

- 총 평가액 = 모든 포지션의 평가액 합
- 총 손익 = 모든 포지션의 손익 합
- 포트폴리오 수익률은 다음 중 하나의 방식으로 정의 (명시 필요):
  1. 단순 평균이 아닌, **원금 가중 수익률**:
     - `total_invested = Σ (buy_price * quantity)`
     - `total_valuation = Σ (current_price * quantity)`
     - `portfolio_return_rate = ((total_valuation - total_invested) / total_invested) * 100`
  2. 기타 방식이 필요하면 별도 명시.

## 에지 케이스 처리

- `buy_price <= 0` 이거나 `quantity < 0`인 입력은 유효하지 않은 데이터로 간주하고 저장을 거부.
- `buy_price > 0`이지만 `current_price`가 없을 경우:
  - 수익률 계산을 시도하지 않고 “시세 없음” 상태로 표시.
- 0으로 나누기 방지:
  - 수익률 계산 시 분모(buy_price)가 0이면 계산하지 않고 에러 또는 특별한 상태로 처리.
