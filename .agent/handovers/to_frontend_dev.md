# Handovers: To Frontend Developer

## 날짜
- 2026-01-16

## 현재 상황 (Context)
- v1.4.0 테마 및 레이아웃 수정 검증 통과(Pass).
- 대시보드 및 모든 서브 페이지에서 사이드바 정상 표시됨.

## 해야 할 일 (Tasks)
- **Minor UI BugFix**:
  1. `Transactions` 테이블: 'Date' 컬럼이 "Invalid Date"로 표시됨. 날짜 포맷팅 함수 확인 필요.
  2. `Positions` 요약 카드: 데이터 없을 시(또는 초기 로드 시) `$NaN`으로 표시됨. 0 또는 '-' 처리 필요.

## 기대 산출물 (Expected Outputs)
- Bugfix Commit
