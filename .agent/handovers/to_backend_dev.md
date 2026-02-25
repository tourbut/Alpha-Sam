# Handovers: To Backend Dev

## 2026-02-25

## 브랜치 (Version Control)
- `feature/dashboard-aggregate-analytics-backend`

## 현재 상황 (Context)
- 대시보드 화면(Allocation 및 Performance History)에 현재 단일 포트폴리오 데이터만 표시되고 있습니다.
- 전체 포트폴리오를 아우르는 합산된 데이터(Total allocation 및 Total history)를 보여주어야 합니다.

## 해야 할 일 (Tasks)
1. `app/src/routes/analytics.py` 에 전체 포트폴리오 합산 Allocation을 가져오는 엔드포인트를 추가하세요. (예: `GET /portfolios/allocation`)
2. `app/src/routes/analytics.py` 에 전체 포트폴리오 합산 History를 가져오는 엔드포인트를 추가하세요. (예: `GET /portfolios/history`)
3. `app/src/services/analytics_service.py` 에 위 엔드포인트에서 호출할 비즈니스 로직(전체 포트폴리오의 자산을 합산하여 비율/기록 계산)을 추가하세요.
4. 추가된 API에 대한 단위 테스트(`tests/test_analytics.py` 또는 관련 테스트 파일)를 작성 및 통과 확인하세요.

## 기대 산출물 (Expected Outputs)
- `GET /portfolios/allocation` 호출 시 `List[AssetAllocationResponse]` 반환.
- `GET /portfolios/history` 호출 시 `List[PortfolioHistoryResponse]` 반환.
- 모든 pytest 케이스 통과.

## 참고 자료 (References)
- `app/src/routes/analytics.py`
- `app/src/services/analytics_service.py`
