# Handovers: To Frontend Dev

## 날짜
- 2026-01-30

## 브랜치 (Version Control)
- `feature/frontend-admin-exchange-rate`

## 현재 상황 (Context)
- 백엔드에서 환율(Exchange Rate) 자산을 지원하게 되었습니다.
- Admin 페이지의 자산 관리(System Assets Management)에서 환율 타입을 선택할 수 있어야 합니다.

## 해야 할 일 (Tasks)
1. **Admin Asset 페이지 수정 (`frontend/src/routes/admin/assets/+page.svelte`)**:
   - `typeOptions` 배열에 `{ value: "EXCHANGE_RATE", name: "Exchange Rate" }` 추가.
   - 자산 추가 모달의 Symbol 입력 필드 아래 도움말(p 태그)에 환율 심볼 예시 추가 (예: `KRW=X` for USD/KRW).

2. **타입 정의 업데이트**:
   - `backend`의 변경 사항에 맞춰 Frontend의 `AdminAsset` 타입 정의(TypeScript Interface)를 업데이트하세요.

## 기대 산출물 (Expected Outputs)
- Admin 페이지에서 `Add Asset` 클릭 시 Type 드롭다운에 `Exchange Rate`가 표시됨.
- `KRW=X` 등으로 자탄 등록 시 정상적으로 요청이 전송됨.

## 참고 자료 (References)
- `frontend/src/routes/admin/assets/+page.svelte`
