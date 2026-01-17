# QA Context Log

- [2025-12-27 10:48:46] 현재 v0.7.0 프론트엔드 기능(User Switcher, Settings, Asset Badges) 검증을 완료하고 대기 중임. Handovers 파일(to_qa_tester.md)은 비어 있음.
- [2025-12-28 20:35:00] v0.8.0 인증 시스템 테스트 계획(Test Plan) 작성을 완료함(.artifacts/projects/qa_reports/test_plan_v0.8.0.md).
- [2025-12-29 23:55:00] v0.8.0 Re-verification 완료. Backend(/users/me) PASS, Frontend(Login Form) PASS. Test Report(.artifacts/projects/qa_reports/test_report_v0.8.0.md) 업데이트 완료.
- [2025-12-31 14:35:00] v0.9.0 마이그레이션 대비 Legacy Data 생성 완료 및 체크리스트 작성함.
- [2025-12-31 15:50:00] v0.9.0 마이그레이션 스크립트 검증 완료(TC-MIG-01).
- [2026-01-01 23:30:00] v1.0.0 Acceptance Setup 진행. Backend Refactoring과 Frontend Polish 통합 검증 완료.
- [2026-01-01 23:35:00] 이슈 발견: Navbar의 Logout 버튼이 동작하지 않음. **Critical Bug**로 보고.
- [2026-01-02 23:55:00] v1.0.0 Acceptance Re-verification 완료. Critical Bug(Logout) 해결 확인.
- [2026-01-07 15:50:00] **v1.0.3 QA FAILED**. 로그인 시 401 에러가 발생하여 대시보드 진입 불가. Remember ID 기능은 동작 확인됨. 테스트 리포트(`test_report_v1.0.3.md`) 작성 후 Developer에게 이슈 전달 필요.
- [2026-01-08 09:35:00] Verify Auth Refactor: **FAILED**. Critical Blocker found. `auth.ts` using Runes must be renamed to `auth.svelte.ts`. Report: `test_report_auth_refactor.md`.
- [2026-01-08 16:05:00] QA Verified: `feature/chat-widget-cleanup`. Navbar Regression, Chat Widget(Mock), Dev Tools Removal all **PASSED**. Report: `test_report_chat_cleanup.md`.
- [2026-01-09 17:05:00] QA Start: `feature/enhanced-mock-chat`. Verifying Dynamic Message History & Auto-scroll.
- [2026-01-09 16:21:00] v1.1.0 Social & Automation 기능 테스트 계획 수립 완료. `.artifacts/projects/qa_reports/test_plan_v1.1.0.md` 생성됨.
- [2026-01-11 21:55:00] v1.2.1 Smoke Test: **FAILED**. Backend `PortfolioCreate` Import 누락으로 인한 가동 중단 문제 발견. QA가 긴급 수정하여 서버 기동했으나, 이후 Login Integration(422 Error) 및 Frontend Route(404) 이슈로 대시보드 진입 불가. 리포트(`test_report_v1.2.0_smoke.md`) 업데이트 완료.
- [2026-01-13 21:47:00] Dashboard Redesign v1.3.0 QA Verification: **PASSED**. Page Title (svelte:head) 누락 발견 후 즉시 수정. 모든 접근성 및 UX 개선 항목 정상 동작 확인. 리포트(`test_report_dashboard_redesign_v1.3.0.md`) 작성 완료.
- [2026-01-15 17:15:00] Theme Refinement v1.4.0 QA: **PARTIAL PASS**. Trusted Professional 테마 스타일은 우수하게 구현되었으나, 사이드바가 대시보드에서만 나타나는 레이아웃 결함 발견. `test_report_theme_refinement_v1.4.0.md` 작성 완료.
- [2026-01-16 11:30:00] Theme Refinement v1.4.0 Re-verification: **PASSED**. Sidebar Layout Issue(Fixed) & Transactions Auth Redirect(Fixed by removing trailing slash in backend). Minor formatting issues noted.
- [2026-01-16 22:05:00] **v1.4.0 Bugfix 검증 완료 (PASS)**.
  - Backend Trailing Slash 이슈 해결 및 Frontend UI(날짜, NaN) 오류 수정 확인.
  - 회귀 테스트 결과 핵심 기능 및 스타일 레이아웃 이상 없음.
  - 리포트: `test_report_v1.4.0_bugfix.md` 작성.

- [2026-01-17 11:35:00] **v1.1.0 Social Features QA 검증 완료 (PASS)**.
  - `feature/social-v1.1.0-frontend` 브랜치 검증.
  - Static Analysis (`npm run check`) 0 Errors 확인 (`settings`, `AssetModal` deprecated events 수정됨).
  - Share Modal, Shared View, Leaderboard UI 로직 및 API 연동 적정성 확인.
  - 리포트: `test_report_v1.1.0_social.md` 작성.
