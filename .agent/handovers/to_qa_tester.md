# Handovers: To QA Tester

## 날짜
- 2026-02-21

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- 주요 기능(멀티 포트폴리오, 자산 트래킹, 인증 등) 릴리즈 및 아키텍처 변경 이후 안정성을 검증하는 종합 기능 테스트 단계입니다.

## 해야 할 일 (Tasks)
1. 현재 시스템의 구조(UUID, 멀티 포트폴리오)를 반영한 E2E 종합 기능 테스트 계획(`test_plan_20260221.md`)을 수립합니다.
2. 사용자 인증, 다중 포트폴리오 조작, 자산 및 거래 추가/삭제, 리더보드 등 핵심 비즈니스 플로우를 브라우저 환경에서 직접 또는 자동화 테스트로 검증합니다.
3. 오류나 동작 이상 발견 시 상세 버그 리포트를 작성하여 프론트/백엔드 담당자가 수정할 수 있도록 리포트합니다.

## 기대 산출물 (Expected Outputs)
- `.agent/project/artifacts/qa_reports/test_plan_20260221.md` (테스트 계획)
- `.agent/project/artifacts/qa_reports/test_report_20260221.md` (종합 테스트 결과 및 버그 내역 리포트)

## 참고 자료 (References)
- `.agent/project/info/domain_rules.md`
- 이전 테스트 리포트 내역들.
