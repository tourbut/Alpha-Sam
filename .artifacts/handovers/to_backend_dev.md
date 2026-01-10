# Handovers: To Backend Developer

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- `PriceService` 리팩토링 및 가격 수집기 분리 작업이 필요합니다.
- Redis는 `cache.py`에 이미 설정되어 있습니다.

## 해야 할 일 (Tasks)
1. **`backend/scripts/price_collector.py` 생성**:
    - Yahoo Finance(`yfinance`)에서 주요 자산(BTC, ETH, AAPL 등 5~10개 샘플) 가격을 수집.
    - Redis Key `price:{SYMBOL}`에 저장.
    - 무한 루프나 간단한 실행 스크립트로 작성 (추후 Cron/Celery 적용 예정).
2. **`backend/app/src/engine/price_service.py` 수정**:
    - `get_current_price` 메서드에서 Yahoo Finance 호출 로직 **제거**.
    - 오직 Redis(`price:{symbol}`)만 조회하도록 변경.
    - Cache Miss 시: `MOCK_PRICES` 반환 (개발 편의성) 또는 0 반환.

## 기대 산출물 (Expected Outputs)
- `python scripts/price_collector.py` 실행 시 Redis에 가격 데이터 적재 확인.
- API 호출 시 `PriceService`가 Redis 데이터를 리턴하는지 확인.

## 참고 자료 (References)
- `backend/app/src/core/cache.py`
- `backend/app/src/engine/price_service.py`
