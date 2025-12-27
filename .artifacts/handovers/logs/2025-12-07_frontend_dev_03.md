# Handovers: To Frontend Developer

## 날짜
2025-12-08

## 현재 상황 (Context)
- QA 리포트(`2025-12-07_qa_report.md`)에 따르면, 백엔드 API는 정상 동작하지만 **자산 목록(`GET /assets`)이 화면에 렌더링되지 않는 버그**가 있습니다.
- 또한, `+layout.svelte`에 네비게이션이 추가되었고, 백엔드에 Redis/Celery 의존성이 추가된 상태입니다.

## 해야 할 일 (Tasks)
1. **자산 목록 렌더링 버그 수정**:
   - `src/routes/assets/+page.svelte` 디버깅.
   - API 응답 데이터가 `assets` 변수에 올바르게 할당되는지, Svelte의 `{#each}` 블록이 정상 동작하는지 확인.
   - `console.log`를 활용하여 데이터 흐름 추적.
2. **시세 정보 표시 (Refine)**:
   - 테이블에 `Current Price`, `Valuation`, `Profit/Loss` 등이 숫자로 잘 표현되는지 확인.
   - 값이 없는 경우(`null` or `undefined`) "-" 로 우아하게 처리.
3. **네비게이션바 확인**:
   - `Assets` 메뉴 클릭 시 페이지 이동이 자연스러운지 확인.

## 기대 산출물 (Expected Outputs)
- `/assets` 접속 시, 등록된 자산 목록이 테이블에 정상적으로 표시되어야 함.
- 브라우저 콘솔에 에러가 없어야 함.

## 참고 자료 (References)
- `.artifacts/handovers/logs/2025-12-07_qa_report.md`
