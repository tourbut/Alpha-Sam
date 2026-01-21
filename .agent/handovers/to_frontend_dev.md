# Handovers: To Frontend Developer

## 날짜
- 2026-01-21

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- 포트폴리오 자산 상세 및 거래 내역 API 연동 완료.
- 현재 대기 중인 프론트엔드 작업 없음.

## 해야 할 일 (Tasks)
1. **Transaction Modal 중복 정리 및 통합**
   - `frontend/src/lib/components/TransactionModal.svelte` (Legacy Svelte 4 style)와 `frontend/src/lib/components/transaction/TransactionFormModal.svelte` (Svelte 5 Runes style)가 중복 존재.
   - `TransactionFormModal.svelte` (Svelte 5 권장)을 기준으로 통합.
   - `frontend/src/routes/assets/+page.svelte`에서 사용 중인 `TransactionModal`을 `TransactionFormModal`로 교체.
   - `createTransaction` API 호출 시 `portfolio_id` 파라미터가 필수이므로, 모달에서 이를 처리하도록 수정 (Props로 받거나 Store 사용).
   - 사용하지 않는 `TransactionModal.svelte` 삭제.

## 기대 산출물 (Expected Outputs)
- `frontend/src/lib/components/transaction/TransactionFormModal.svelte`로 통합된 모달 컴포넌트.
- `TransactionModal.svelte` 파일 삭제.
- 자산 목록 페이지 및 포트폴리오 상세에서 트랜잭션 추가 기능 정상 동작.
