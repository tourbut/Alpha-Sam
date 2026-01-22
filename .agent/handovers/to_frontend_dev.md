# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/frontend-asset-list-refresh` (from `develop`)

## 현재 상황 (Context)
- 포트폴리오 상세 페이지(`portfolios/[id]`)에서 자산을 추가(`Add Asset`)해도 목록에 즉시 표시되지 않음.
- `<AssetModal>` 컴포넌트의 `created` 이벤트를 부모 페이지에서 처리하지 않아서 발생하는 문제.

## 해야 할 일 (Tasks)
1. `src/routes/portfolios/[id]/+page.svelte` 수정:
   - `<AssetModal>` 컴포넌트 선언부에 `on:created={loadAssets}` 속성 추가.
   - 자산 추가 모달이 닫히면서 `created` 이벤트 발생 시 `loadAssets()` 함수가 호출되어 목록이 갱신되어야 함.

## 기대 산출물 (Expected Outputs)
- 포트폴리오 상세 페이지에서 자산 추가 완료 후 즉시 목록에 새 자산이 표시됨.
