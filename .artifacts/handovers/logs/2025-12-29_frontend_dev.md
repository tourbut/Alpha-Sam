# Handovers: To Frontend Developer

## 날짜
2025-12-29

## 브랜치 (Version Control)
- `feature/frontend-auth-research`

## 현재 상황 (Context)
- Backend에서 `fastapi-users` 기반의 표준 JWT 인증 API를 구현 중입니다 (v0.8.0).
- `UserSwitcher` (개발용) 컴포넌트는 폐기될 예정입니다.

## 해야 할 일 (Tasks)
1. **Design**:
   - 로그인 (`/login`) 및 회원가입 (`/register`) 페이지 UI 구현.
   - TailwindCSS 기반의 깔끔한 Form 디자인.
2. **Integration Research**:
   - Backend API (`/auth/jwt/login`, `/auth/register`)와의 연동 방식 설계.
   - JWT 토큰 저장 전략 (LocalStorage vs Cookie) 결정 및 구현.
   - 인증 상태(Auth Store) 관리: 로그인 여부에 따른 GNB(메뉴) 변화 처리.
3. **Cleanup**:
   - `UserSwitcher` 컴포넌트 제거 준비.

## 기대 산출물 (Expected Outputs)
- 로그인/회원가입 퍼블리싱 페이지.
- 인증 관련 Store 로직 초안.

## 참고 자료 (References)
- Backend가 구현할 API 명세는 `fastapi-users` 표준을 따릅니다.

---

# Bugfix Handover (Completed)
## 날짜
2025-12-29 (Bugfix)

## 해야 할 일 (Tasks)
1. **Critical Bugfix (Login Form)**:
   - `src/routes/login/+page.svelte` 확인.
   - `<form>` 태그의 `on:submit` 이벤트 핸들러가 `preventDefault`를 제대로 수행하는지 확인.
   - `method="POST"`를 명시하거나, Svelte의 `on:submit|preventDefault` 수식어 사용 확인.
2. **Integration Verification**:
   - 수정 후 로컬 브라우저에서 로그인 시도 -> URL 쿼리 파라미터가 붙지 않아야 함.

## 결과
- `frontend/src/routes/login/+page.svelte` 수정 완료: `method="POST"` 추가.
