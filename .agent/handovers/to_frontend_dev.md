# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/frontend-asset-creation` (from `develop`)

## 현재 상황 (Context)
- 자산 추가(`Add Asset`) 시 `422 Unprocessable Content` 에러 발생.
- `AssetModal.svelte`에서 `createAsset` API 호출 시 필수 필드인 `symbol`이 누락된 것으로 확인됨.

## 해야 할 일 (Tasks)
1. `src/lib/components/AssetModal.svelte` 수정:
   - `handleSubmit` 함수 내 `createAsset` 호출 인자에 `symbol` 필드 추가.
2. (선택사항) 자산 추가 후 목록 자동 갱신(`dispatch('created')`)이 잘 동작하는지 확인.

## 기대 산출물 (Expected Outputs)
- 자산 추가 모달에서 "Create Asset" 클릭 시 422 에러 없이 자산이 정상 생성되어야 함.
