# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/frontend-asset-lookup` (from `develop`)

## 현재 상황 (Context)
- Backend에서 자산 조회(`get_asset_by_symbol` 등) 시 `portfolio_id`가 필수(또는 권장) 파라미터로 변경될 예정.
- 포트폴리오별로 동일한 심볼(예: AAPL)을 가질 수 있으므로 정확한 조회를 위해 필요.

## 해야 할 일 (Tasks)
1. 자산 정보를 조회하는 로직(예: `getAssetBySymbol` API 호출부) 확인.
   - 위치 예상: `AssetModal.svelte` 또는 자산 상세 페이지 등.
2. 해당 API 호출 시 현재 선택된 `portfolio_id`를 파라미터로 함께 전달하도록 수정.
   - (참고: Backend API가 Query Parameter 등으로 `portfolio_id`를 받도록 수정될 것임)

## 기대 산출물 (Expected Outputs)
- 자산 조회 기능이 포트폴리오 컨텍스트에 맞게 정확히 동작함.
