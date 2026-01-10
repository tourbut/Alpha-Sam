# Handovers: To Frontend Developer

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- 백엔드 `PriceService`가 대대적으로 리팩토링될 예정입니다 (Live API -> Redis).
- 개발 도중 `/api/v1/market/prices/*` 엔드포인트가 일시적으로 Mock 데이터를 반환하거나 0을 반환할 수 있습니다.

## 해야 할 일 (Tasks)
1. **대기 및 모니터링**:
    - 백엔드 작업 완료 시까지 대시보드 가격 표시가 이상할 수 있음을 인지.
    - 별도의 코드 수정 사항은 현재 없습니다.

## 기대 산출물 (Expected Outputs)
- N/A

## 참고 자료 (References)
- `.artifacts/handovers/to_backend_dev.md`
