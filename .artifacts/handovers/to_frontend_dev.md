# Handovers: To Frontend Developer

## 날짜
2025-12-27

## 브랜치 (Version Control)
- `feature/frontend-auth-research`

## 현재 상황 (Context)
- v0.7.0 완료. v0.8.0에서는 모의 유저 전환(User Switcher)을 제거하고 실제 JWT 기반 로그인을 도입합니다.

## 해야 할 일 (Tasks)
1. `feature/frontend-auth-research` 브랜치 생성.
2. SvelteKit에서 JWT 처리 방식 조사.
   - 쿠키(HttpOnly) 방식 vs 헤더(LocalStorage) 방식 장단점 및 구현 난이도 검토.
   - SSR(Server-Side Rendering) 시 인증 정보 유지 방법 확인 (`hooks.server.ts` 등).
3. 현재 `UserSwitcher` 및 `user_id` 관련 로직이 사용되는 컴포넌트 파악.
4. 로그인(Login) / 회원가입(Register) 페이지 UI 구조 구상 (스케치).

## 기대 산출물 (Expected Outputs)
- 인증 구현 방식에 대한 의견/계획서 (간단한 MD 파일).
- 로그인/회원가입 페이지 와이어프레임 또는 스케치.

## 참고 자료 (References)
- SvelteKit Auth Best Practices
