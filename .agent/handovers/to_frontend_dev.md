# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/frontend-portfolio-refresh` (from `develop` or `main`)

## 현재 상황 (Context)
- 포트폴리오 생성(`Create Portfolio`) 후 목록 화면(`portfolios/+page.svelte`)이 즉시 갱신되지 않고 새로고침해야만 반영되는 문제 발생.

## 해야 할 일 (Tasks)
1. `src/lib/components/portfolio/CreatePortfolioModal.svelte` 수정:
   - 포트폴리오 생성(API 성공) 후, 부모 컴포넌트에 알리기 위해 `dispatch('created')` 이벤트 발생 로직 추가.
2. `src/routes/portfolios/+page.svelte` 수정:
   - `<CreatePortfolioModal>` 컴포넌트 사용 부분에 `on:created={...}` 이벤트 핸들러 추가.
   - 핸들러 내에서 `portfoliosWithAssets` 목록을 다시 불러오는 함수(`fetchPortfoliosWithAssets` 등) 호출.

## 기대 산출물 (Expected Outputs)
- 포트폴리오 생성 모달이 닫힌 후, 페이지 새로고침 없이 즉시 새로운 포트폴리오 카드가 목록에 표시되어야 함.
