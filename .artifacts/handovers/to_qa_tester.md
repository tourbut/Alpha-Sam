# Handovers: To QA Tester

## 날짜
- 2026-01-11

## 현재 상황 (Context)
- v1.2.0 배포 절차가 진행 중입니다.
- 배포 완료 후 최종 운영 환경 검증(Smoke Test)이 필요합니다.

## 해야 할 일 (Tasks)
1. **Standby**: DevOps의 배포 완료 신호 대기.
2. **Post-Deployment Verification**:
    - `main` 브랜치(또는 배포 환경)에서 핵심 시나리오(로그인 -> 대시보드 -> 포트폴리오 생성 -> 매수) 정상 동작 확인.
    - 기존 데이터(Default Portfolio)가 정상적으로 보이는지 확인.

## 기대 산출물 (Expected Outputs)
- `test_report_v1.2.0_post_deployment.md`

## 참고 자료 (References)
- `.artifacts/projects/qa_reports/test_report_v1.2.0_20260111.md`
