# Handovers: To Frontend Developer

## 날짜
2025-12-08

## 현재 상황 (Context)
- QA 테스트 결과, **UI 데이터 로딩 실패** 및 **Svelte 5 호환성 문제**가 발견되었습니다.
- 백엔드 API (`/api/v1/assets/`)는 정상적으로 데이터를 반환합니다.
- 임시 핫픽스(`+layout.svelte`)가 적용되어 대시보드 진입은 가능합니다.

## 이슈 및 해야 할 일 (Tasks & Issues)
1. **데이터 로딩 문제 해결 (Critical)**
   - 증상: `/assets`에서 "No assets found", 대시보드에서 "Loading..." 상태 지속.
   - 단서: `curl http://localhost/api/v1/assets/`는 200 OK. 브라우저에서 `fetch`가 실패하는 원인을 찾아야 함. `api.ts`에 Trailing Slash는 추가됨.
   - 액션: 브라우저 개발자 도구 네트워크 탭 분석 후 수정.

2. **Navbar Svelte 5 호환성 수정**
   - 증상: `let:hidden let:toggle` 사용 시 `invalid_default_snippet` 에러 발생. 현재 핫픽스로 해당 지시어를 제거하여 모바일 메뉴 토글 불가.
   - 액션: `flowbite-svelte` 버전에 맞는 Navbar 구현으로 수정.

3. **포지션 삭제 기능 추가** (이전 요청 사항 유지).

## 기대 산출물 (Expected Outputs)
- 데이터가 정상적으로 표시되는 대시보드.
- 모바일 메뉴가 동작하는 Navbar.

## 참고 자료 (References)
- QA 리포트: `.artifacts/handovers/logs/2025-12-08_qa_report_2.md`
