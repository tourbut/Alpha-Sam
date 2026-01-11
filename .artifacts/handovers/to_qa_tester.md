# Handovers: To QA Tester

## 날짜
- 2026-01-11

## 현재 상황 (Context)
- v1.2.0 배포가 완료되었습니다(Tag v1.2.0, DB Migrated).
- 운영 환경(Production)에서의 최종 점검(Smoke Test)이 필요합니다.

## 해야 할 일 (Tasks)
1. **Smoke Test Execution**:
    - **Login**: 정상 로그인 확인.
    - **Dashboard**: "Main Portfolio"가 기본 선택되어 있고, 포지션이 로딩되는지 확인.
    - **Transaction**: "Add Transaction" (매수) 시도 후 포지션 수량/평단가 업데이트 확인.
    - **Multi-Portfolio**: "Create Portfolio"로 새 포트폴리오 생성 및 전환 확인.
2. **Report**: 테스트 결과를 리포트로 작성.

## 기대 산출물 (Expected Outputs)
- `.artifacts/projects/qa_reports/test_report_v1.2.0_smoke.md`

## 참고 자료 (References)
- `.artifacts/projects/deployment_checklist_v1.2.0.md`
