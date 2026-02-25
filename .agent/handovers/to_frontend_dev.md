# Handovers: To Frontend Dev

## 2026-02-25

## 브랜치 (Version Control)
- `feature/dashboard-aggregate-analytics-frontend`

## 현재 상황 (Context)
- 대시보드 뷰(`frontend/src/routes/+page.svelte`)가 현재 단일 특정 포트폴리오(`currentPortfolio`)의 Allocation과 History 데이터만 요청하여 보여주고 있습니다.
- 대시보드 목적에 맞게, 전체 포트폴리오에 대한 통합(Aggregated) 정보를 요청하고 렌더링하도록 수정해야 합니다. 백엔드에서 제공할 새로운 엔드포인트를 적용해야 합니다.

## 해야 할 일 (Tasks)
1. `frontend/src/lib/apis/analytics.ts` 파일에 새로운 통합 데이터 API 함수 추가.
   - 예: `get_portfolios_allocation` (`GET /portfolios/allocation`)
   - 예: `get_portfolios_history` (`GET /portfolios/history`)
2. `frontend/src/routes/+page.svelte` 수정.
   - 기존의 `get_portfolio_allocation({ portfolio_id: currentPortfolio.id })` 와 `get_portfolio_history({ portfolio_id: currentPortfolio.id })` 대신 **새로 추가한 전체 포트폴리오용 함수**를 호출하도록 변경.
3. 데이터 응답이 정상적으로 Allocation 차트와 History 차트에 렌더링되는지 확인.

## 기대 산출물 (Expected Outputs)
- 대시보드의 파이 차트 및 수익률 차트에 사용자의 "전체" 자산 분포 및 히스토리가 요약되어 표시될 것.
- API 호출 시 오류가 없으며 타입 에러(Svelte Check)가 통과할 것.

## 참고 자료 (References)
- `frontend/src/routes/+page.svelte`
- `frontend/src/lib/apis/analytics.ts`
