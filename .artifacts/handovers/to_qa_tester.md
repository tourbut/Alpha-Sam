# Handovers: To QA Tester

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- Frontend 팀에서 `auth` store를 Svelte 5 Runes로 리팩토링 진행 예정입니다.
- 이로 인해 인증(로그인/로그아웃) 로직의 내부 구현이 변경되므로, 기능 회귀 테스트가 필요합니다.

## 해야 할 일 (Tasks)
1. 로그인 기능 테스트:
   - 올바른 자격 증명으로 로그인 성공 여부 확인.
   - 대시보드 접근 가능 여부 확인.
2. 상태 유지 테스트:
   - 로그인 상태에서 브라우저 새로고침 시 로그인 상태가 유지되는지 확인.
3. 로그아웃 기능 테스트:
   - 로그아웃 버튼 클릭 시 토큰 삭제 및 로그인 페이지 리다이렉트 확인.
4. "Remember ID" 기능 (이전 구현)이 여전히 잘 동작하는지 확인.

## 기대 산출물 (Expected Outputs)
- QA Report에 테스트 결과(Pass/Fail) 기록.

## 참고 자료 (References)
- `frontend/src/lib/stores/auth.ts`
