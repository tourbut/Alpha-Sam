# Real-time Price API Analysis

## 1. 배경
현재 `PriceService`는 랜덤한 Mock 데이터를 반환하고 있습니다. Alpha-Sam 서비스의 신뢰도를 높이기 위해 실제 시장 데이터(Crypto & Stocks)를 연동해야 합니다.
프로젝트 성격(개인 포트폴리오/토이 프로젝트 추정)상 **무료(Free Tier)** 이거나 **비용 효율적인** 솔루션이 우선됩니다.

## 2. 후보 서비스 분석

### Option A: CoinGecko API (Crypto Only)
- **URL**: https://api.coingecko.com/api/v3/
- **데이터 범위**: 암호화폐 전반 (주식 미지원).
- **가격 정책**: 
  - **Demo Plan (Free)**: 분당 30회 호출 제한 (Rate Limit). API Key 불필요(Public) 혹은 필요할 수 있음(정책 변경 잦음).
- **장점**: 암호화폐 커버리지가 가장 넓고 데이터 품질이 우수. 별도 가입 없이 바로 테스트 가능.
- **단점**: 주식(AAPL, TSLA 등) 데이터 부재. 분당 30회는 다수 사용자가 동시에 접속 시 부족할 수 있음.

### Option B: Yahoo Finance (yfinance Library)
- **방식**: `yfinance` 파이썬 라이브러리 사용 (Unofficial API Wrapper).
- **데이터 범위**: 전 세계 주식, ETF, 암호화폐, 환율.
- **가격 정책**: 무료 (Open Source 라이브러리).
- **장점**: 주식과 코인을 모두 지원. 구현이 매우 간편함 (`yf.Ticker("AAPL").history()`). 비용 "0".
- **단점**: 공식 API가 아니므로 불안정할 수 있음(Scraping 기반). 속도가 다소 느릴 수 있음. 상업적 이용 시 라이선스 이슈 주의 필요.

### Option C: Finnhub.io
- **URL**: https://finnhub.io/
- **데이터 범위**: 미국 주식, Forex, Crypto.
- **가격 정책**: Free Tier - 분당 60회 호출.
- **장점**: 주식/크립토 통합 API 제공. 공식 API라 안정적.
- **단점**: 한국 주식 등 마이너한 자산 커버리지 확인 필요. Crypto 종류가 CoinGecko보다 적음.

## 3. 기술적 과제 및 해결 방안

### 3.1 Rate Limit 핸들링
무료 API는 호출 제한이 엄격합니다(예: 30~60 calls/min). 사용자가 대시보드를 새로고침할 때마다 외부 API를 호출하면 금방 차단당합니다.

**전략: Server-side Caching (현재 구조 유지 및 강화)**
- **구조**: `Client` -> `Backend (PriceService)` -> `Redis Cache` -> `External API`
- **로직**:
    1. 요청 시 Redis 캐시 확인.
    2. 캐시 유효(Time-to-Live: 예 60초~5분)하면 캐시 값 리턴.
    3. 캐시 만료 시에만 외부 API 호출 후 캐시 갱신.
- **효과**: 사용자 수가 늘어도 외부 API 호출 횟수는 `(자산 수) / (TTL)` 빈도로 고정됨.

### 3.2 Ticker Mapping
외부 서비스마다 심볼 표기법이 다를 수 있습니다.
- DB 저장: `BTC`
- CoinGecko: `bitcoin` (ID 기준)
- Yahoo: `BTC-USD`

**해결**: `Asset` 모델 혹은 설정 파일에 `api_id` 매핑 필드를 추가해야 할 수도 있음.
- *v0.3.0 단계에서는 심볼 변환 로직을 Service 내부에 하드코딩하거나 딕셔너리로 관리하는 것을 추천.*

## 4. 제안 아키텍처 (Hybrid Strategy)

가장 비용 효율적이고 커버리지가 넓은 **Hybrid 방식**을 제안합니다.

1.  **Crypto**: **CoinGecko** (또는 yfinance가 안정적이면 yfinance로 통합 가능)
2.  **Stocks**: **yfinance** 라이브러리 (비공식적이지만 개인 프로젝트에 적합)
    - *대안*: 안정성이 중요하다면 **Finnhub** 사용.

**추천 구현 (1단계): `yfinance` 라이브러리 단일 사용**
- 이유: 주식과 코인을 동시에 조회할 수 있어 코드가 깔끔해짐 (`AAPL`, `BTC-USD`). 별도 API Key 관리 불필요.
- 구현 난이도가 가장 낮음.

### PriceService Pseudocode (`yfinance` 적용 시)

```python
import yfinance as yf

async def get_real_price(symbol: str):
    # Symbol Correction (e.g., BTC -> BTC-USD for Yahoo)
    if symbol in ["BTC", "ETH", "SOL"]:
        query_symbol = f"{symbol}-USD"
    else:
        query_symbol = symbol

    ticker = yf.Ticker(query_symbol)
    # 비동기 처리가 아니므로 blocking 방지를 위해 run_in_executor 사용 고려
    data = ticker.history(period="1d")
    current_price = data['Close'].iloc[-1]
    return current_price
```

## 5. 결론 및 Next Step
- **결론**: **`yfinance` 라이브러리를 사용한 통합 조회**로 시작.
- **Next Step**:
    - `PriceService` 내부 로직을 `yfinance` 기반으로 변경.
    - Redis Caching TTL(유효시간)을 60초~180초 정도로 설정하여 API 부하 방지.
    - 블로킹 I/O 이슈(yfinance는 동기 라이브러리) 해결을 위해 `asyncio.to_thread` 등 사용 필요.
