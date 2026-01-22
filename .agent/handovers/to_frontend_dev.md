# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/frontend-type-errors-and-assets` (from `develop`)

## 현재 상황 (Context)
- PR #15(코드 정리) 이후 QA 검증 결과, 기능상 회귀는 없으나 **23개의 기존 타입 에러**와 **/assets 페이지 데이터 미표시** 이슈가 발견되었습니다.
- 안정적인 빌드와 사용자 경험을 위해 이 문제들의 수정이 시급합니다.

## 해야 할 일 (Tasks)

### 1. 타입 에러 수정 (Priority: High)
`npm run check`를 실행하여 다음 에러들을 해결하세요:
1.  **AssetModal Prop 누락**:
    -   `src/routes/+layout.svelte` 및 `portfolios/[id]/+page.svelte`에서 `<AssetModal>` 사용 시 `portfolioId`가 누락된 문제 수정 (Optional 처리 또는 조건부 렌더링).
2.  **타입 추론 오류**:
    -   `src/routes/portfolios/[id]/+page.svelte`: `assets` 배열이 `never[]`로 추론되는 문제. 명시적 인터페이스/타입 정의 후 할당.
3.  **API 호출 인자 불일치**:
    -   `src/routes/transactions/+page.svelte`: `createTransaction` 함수 호출 시 인자 개수/타입 1일치.
4.  **Flowbite-Svelte 호환성**:
    -   `FollowButton.svelte`: `flowbite-svelte/dist/types` import 경로 확인 및 수정.
    -   `Spinner` 컴포넌트의 `size` prop 타입(`"lg"` 등 문자열 vs 숫자) 호환성 수정.

### 2. Assets 페이지 (`/assets`) 기능 정상화 (Priority: High)
1.  `/assets` 경로 접속 시 "No assets found"가 표시되는 원인 분석.
    -   현재 전역 자산(모든 포트폴리오의 자산 합계)을 가져오는 API(`GET /api/v1/assets` 등)가 제대로 연동되어 있는지 확인.
2.  데이터가 정상적으로 표시되도록 수정.

## 기대 산출물 (Expected Outputs)
- `npm run check` 실행 시 에러 0개.
- `/assets` 페이지에서 사용자가 보유한 자산 목록이 정상적으로 표시될 것.
