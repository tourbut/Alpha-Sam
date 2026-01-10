# Handovers: To QA Tester

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- 백엔드 `PriceService` 구조가 변경됩니다 (Yahoo Finance 직접 호출 제거).

## 해야 할 일 (Tasks)
1. **테스트 시나리오 준비**:
    - Redis에 데이터가 없을 때, API가 에러 없이 Mock/Default 값을 반환하는지.
    - `price_collector.py` 실행 후, API가 정상적으로 Redis 값을 반환하는지.
    - 데이터가 갱신(TTL 만료)되는지 확인.

## 기대 산출물 (Expected Outputs)
- QA Test Case 문서 업데이트 (Redis 의존성 추가).

## 참고 자료 (References)
- `.artifacts/handovers/to_backend_dev.md`
