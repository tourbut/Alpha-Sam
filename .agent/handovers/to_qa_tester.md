# Handovers: To QA Tester

## 날짜
- 2026-01-16

## 현재 상황 (Context)
- Frontend(v1.4.0) 및 Backend(Router Fix) 작업들이 진행/완료됨.
- Frontend에서 `Transactions` 날짜 표시 오류 및 `Positions` NaN 표시 오류 수정 예정.

## 해야 할 일 (Tasks)
1. **Verify Backend Trailing Slash Fix**:
   - `Transactions` API 및 기타 라우터들이 Trailing Slash 여부와 관계없이 정상 동작하는지 검증 (`test_slash.py` 활용 권장).
2. **Verify Frontend v1.4.0 Bugfixes**:
   - Frontend 작업 완료 시, `Transactions` 페이지 날짜 포맷 확인.
   - `Positions` 요약 카드 데이터(NaN) 확인.
3. **Regression Test**:
   - v1.4.0 변경사항(테마, 레이아웃)이 기존 기능(로그인, 대시보드 그래프 등)에 사이드 이펙트를 주지 않았는지 확인.

## 기대 산출물 (Expected Outputs)
- `qa_reports/test_report_v1.4.0_bugfix.md`

## 참고 자료 (References)
- `.agent/handovers/to_frontend_dev.md`
- `.agent/handovers/to_backend_dev.md`
