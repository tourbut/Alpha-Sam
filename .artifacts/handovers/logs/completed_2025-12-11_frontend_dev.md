# Handovers: To Frontend Developer (Completed)

## 날짜
2025-12-11

## 현재 상황 (Context)
- 백엔드 인증 API (`/auth/login`, `/auth/signup`)가 준비되었습니다.
- 이제 사용자 로그인/회원가입 인터페이스를 구현해야 합니다.
- (Update 1) 네비게이션 바 UX 개선 및 첫 화면 리다이렉트 요청 처리.
- (Update 2) 데이터 시각화(Chart) 기능 추가 요청 처리.

## 해야 할 일 (Tasks)
1. **로그인 페이지 (`/login`) 구현**:
   - 이메일/비밀번호 입력 폼.
   - `POST /api/v1/auth/login` 연동.
   - 성공 시 JWT 토큰 저장 (localStorage 추천) 및 메인으로 이동.

2. **회원가입 페이지 (`/signup`) 구현**:
   - 이메일/비밀번호 입력 폼.
   - `POST /api/v1/auth/signup` 연동.
   - 성공 시 로그인 페이지로 이동 또는 자동 로그인.

3. **인증 상태 관리**:
   - 토큰 유무에 따른 헤더 변경 (로그인/로그아웃 버튼).
   - 로그아웃 기능 (토큰 삭제).

4. **네비게이션 바 상단 고정 (Fixed Navbar)**:
   - `src/routes/+layout.svelte` 수정.
   - Navbar가 화면 상단에 항상 고정되도록 CSS/Flowbite 옵션 조정 (`sticky top-0 z-50` 등).
   - 본문 컨텐츠가 네비게이션 바에 가려지지 않도록 상단 패딩(`pt-*`) 추가 필요.

5. **첫 화면을 로그인 화면으로 변경**:
   - 비로그인 사용자가 `/` 접속 시 자동으로 `/login`으로 리다이렉트되도록 수정.
   - `src/routes/+page.svelte`의 `onMount` 또는 `script` 블록에서 인증 상태 확인 후 처리.

6. **데이터 시각화 (Charts) 추가**:
   - `chart.js` 설치 (svelte-chartjs는 Svelte 5 호환성 문제로 제외).
   - **Pie Chart (포트폴리오 구성)**: `src/lib/components/PortfolioDistributionChart.svelte` 구현.
   - **Line Chart (수익률 추이 - Mock)**: `src/lib/components/PortfolioHistoryChart.svelte` 구현.
   - 대시보드(`/`)에 차트 섹션 추가.

## 완료 내역 (Implemented)
- Login page: `src/routes/login/+page.svelte` verified.
- Signup page: `src/routes/signup/+page.svelte` verified.
- Auth State: `src/lib/stores/auth.ts` verified.
- Navbar/Footer: Updated in `src/routes/+layout.svelte`.
- Fixed Navbar: Added `fixed w-full z-20 top-0` to Navbar and `pt-20` to main in `+layout.svelte`.
- Redirect: Added auth check and redirect logic to `+page.svelte` onMount.
- **Charts Added**: Installed `chart.js`.
  - Added `PortfolioDistributionChart` (Pie) using dynamic position data.
  - Added `PortfolioHistoryChart` (Line) using mock data.
  - Integrated into Dashboard grid layout.
- `npm run check` passed.
