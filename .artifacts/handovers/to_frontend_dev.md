# Handovers: To Frontend Developer

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- 현재 `frontend/src/lib/stores/auth.ts`는 Svelte 4 스타일의 `writable` store를 사용하고 있습니다.
- 이를 최신 Svelte 5 Runes 문법(`$state`)으로 리팩토링하여 성능과 DX를 개선하고자 합니다.
- 사용자 요청에 따라 "완벽하게" 수행해야 하며, 이를 사용하는 파일들도 함께 수정해야 합니다.

## 해야 할 일 (Tasks)
1. `frontend/src/lib/stores/auth.ts` 리팩토링:
   - `writable`을 제거하고 `$state`를 사용하여 반응형 상태를 정의하십시오. (예: `class AuthState` 패턴)
   - `isAuthenticated`, `token`, `user` 상태를 관리하십시오.
   - `login`, `logout`, `initialize`, `updateUser` 메서드를 구현하여 상태 변경 및 `localStorage` 동기화를 처리하십시오.
   - 예시 구조:
     ```typescript
     class AuthState {
         isAuthenticated = $state(false);
         // ...
         constructor() {
             this.initialize();
         }
         // methods...
     }
     export const auth = new AuthState();
     ```
     (참고: SSR 환경에서직접 `new` 호출 시 주의가 필요하다면 `initialize`를 명시적으로 호출하거나 안전한 패턴을 사용하십시오. SvelteKit에서는 모듈 사이드 이펙트로 전역 상태를 만들면 서버에서 공유될 수 있으나, 현재 `auth.ts`는 클라이언트 상태(localStorage) 위주이므로 브라우저 체크 (`if (browser)`)가 중요합니다.)

2. `frontend/src/lib/fastapi.js` 수정:
   - `import { get } from 'svelte/store';` 제거.
   - `get(auth)` 호출을 제거하고 `auth.token` 등에 직접 접근하도록 변경하십시오.

3. `.svelte` 컴포넌트 수정 (`routes/login/+page.svelte`, `layout.svelte` 등):
   - `$auth` (store 구독 문법) 사용처를 모두 찾아 `auth.프로퍼티` (예: `auth.isAuthenticated`) 접근으로 변경하십시오.
   - `$auth.user` -> `auth.user`

4. 동작 검증:
   - 로컬 서버(`npm run dev`)에서 로그인/로그아웃, 새로고침 시 상태 유지(Persist)가 정상 동작하는지 확인하십시오.

## 기대 산출물 (Expected Outputs)
- `frontend/src/lib/stores/auth.ts` 파일이 Runes 문법으로 변경됨.
- `frontend/src/lib/fastapi.js` 및 관련 컴포넌트들이 에러 없이 동작함.
- 애플리케이션 로그인/로그아웃 기능이 정상 작동함.

## 참고 자료 (References)
- [Svelte 5 Runes Documentation](https://svelte.dev/docs/svelte/runes)
- `frontend/src/lib/stores/auth.ts` (기존 코드)
