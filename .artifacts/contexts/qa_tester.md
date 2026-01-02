# QA Context Log

- [2025-12-27 10:48:46] 현재 v0.7.0 프론트엔드 기능(User Switcher, Settings, Asset Badges) 검증을 완료하고 대기 중임. Handovers 파일(to_qa_tester.md)은 비어 있음.

- [2025-12-28 20:35:00] v0.8.0 인증 시스템 테스트 계획(Test Plan) 작성을 완료함(.artifacts/projects/qa_reports/test_plan_v0.8.0.md). 회원가입, 로그인, 로그아웃, 토큰 관리 등 주요 시나리오를 포함.
- [2025-12-29 23:55:00] v0.8.0 Re-verification 완료. Backend(/users/me) PASS, Frontend(Login Form) PASS. Test Report(.artifacts/projects/qa_reports/test_report_v0.8.0.md) 업데이트 완료.
- [2025-12-31 14:35:00] v0.9.0 마이그레이션 대비 Legacy Data(Asset ID=11 with NULL owner) 생성 완료 및 체크리스트(checklist_v0.9.0.md) 작성함.
- [2025-12-31 15:50:00] v0.9.0 마이그레이션 스크립트 검증 완료(TC-MIG-01). `NOT NULL` 제약조건 일시 해제 후 Dirty Data 주입 -> Migration -> 검증 성공. Test Report 작성함.
- [2026-01-01 23:30:00] v1.0.0 Acceptance Setup 진행. Backend Refactoring(Service layer)과 Frontend Polish(UI) 통합 검증 완료. `test_report_v1.0.0.md` 작성.
- [2026-01-01 23:35:00] 이슈 발견: Navbar의 Logout 버튼이 동작하지 않음(Session Persistence Issue). **Critical Bug**로 보고하고 Frontend에 수정을 요청해야 함.
- [2026-01-02 23:55:00] v1.0.0 Acceptance Re-verification 완료. Critical Bug(Logout) 해결 확인(TC-V1-05 PASS). Test Report를 PASS로 업데이트하고 Release 준비 상태로 전환함.
