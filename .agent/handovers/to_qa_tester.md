# Handovers: To QA Tester

## 날짜
- 2026-02-21

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- `Position` 데이터가 DB 테이블에서 제거되고 실시간 계산되는 방식으로 구조가 변경되었습니다. 

## 해야 할 일 (Tasks)
1. 사용자가 거래(Transaction)를 추가하거나 삭제할 때, 포트폴리오의 잔고(Position) 및 총 평가액, 수익률이 즉각적이고 정확하게 반영되는지 집중적으로 E2E 브라우저 테스트를 수행하세요.
2. (공매도 불가) 보유 수량보다 많은 자산을 "매도"하려고 할 때 시스템이 적절하게 차단하고 오류 메시지를 보여주는지 화면에서 확인하세요.
3. 테스트 결과를 `.agent/project/artifacts/qa_reports/test_report_20260221_position.md` 파일로 작성하세요.

## 기대 산출물 (Expected Outputs)
- 트랜잭션-포지션 계산 파이프라인 E2E 테스트 통과 확인.
- 상세한 버그 리포트 (발견 시).

## 참고 자료 (References)
- `.agent/handovers/to_backend_dev.md`
- `.agent/handovers/to_frontend_dev.md`
