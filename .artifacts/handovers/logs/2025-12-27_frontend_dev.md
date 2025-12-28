
## [2025-12-27 Handovers]
### Tasks from to_frontend_dev.md
# Handovers: To Frontend Developer

## 날짜
2025-12-27

## 브랜치 (Version Control)
- `feature/frontend-auth-v0.8.0` (create from `develop`)

## 현재 상황 (Context)
- v0.8.0 인증 시스템 기획 완료.
- `UserSwitcher`를 제거하고 실제 로그인을 구현해야 합니다.

## 해야 할 일 (Tasks)
1. **Auth Store 구현**:
   - `src/lib/stores/auth.ts`: Writable Store로 `user`, `accessToken` 상태 관리 (LocalStorage 연동).
2. **페이지 구현**:
   - `/login`, `/register`: 이메일/비밀번호 입력 폼 및 백엔드 연동.
   - `/`: 로그인 안 된 상태면 `/login`으로 리다이렉트 (Client-side Check).
3. **API 모듈 수정**:
   - `src/lib/api.ts`: `X-User-Id` 헤더 제거.
   - `Authorization: Bearer <token>` 헤더 자동 삽입 로직 추가.
   - 401 응답 시 로그인 페이지로 강제 이동 및 토큰 삭제 처리.
4. **UI 업데이트**:
   - 상단 네비게이션 바에 로그인 유저 정보 및 로그아웃 버튼 표시.
   - 기존 `UserSwitcher` 컴포넌트 제거.

## 기대 산출물 (Expected Outputs)
- 로그인/회원가입이 가능한 웹 인터페이스.
- 새로고침 해도 로그인이 유지되는지 확인 (LocalStorage).

## 참고 자료 (References)
- `.artifacts/v0.8.0_implementation_plan.md`

### Result
- **Status**: Completed
- **Branch**: `feature/frontend-auth-v0.8.0`
- **Changes**:
  - Implemented `lib/stores/auth.ts` with localStorage sync.
  - Updated `lib/api.ts` to use `fetchWithAuth`, handle 401, remove `X-User-Id`.
  - Updated `+layout.svelte` for client-side redirect and Auth UI, removed `DevUserSwitcher`.
  - Removed `DevUserSwitcher` component/store.
  - Verified `login` and `signup` pages exist and use updated API/Store.
