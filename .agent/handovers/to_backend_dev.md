# Handovers: To Backend Dev

## 날짜
- 2026-02-21

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- Architect가 `Position` 모델(DB 테이블)을 제거하는 작업을 완료했습니다. 이제 포지션 정보는 `Transaction` 내역 기반으로 런타임에 동적 계산됩니다.
- 현재 루트 하위 `tests/`와 `app/tests/` 등에 동일한 이름의 테스트 파일들이 존재하여 Pytest가 테스트 모듈을 수집(Collection)하는 과정에서 Import Mismatch 오류가 발생하며 멈추는 상태입니다.

## 해야 할 일 (Tasks)
1. 중복된 이름의 테스트 파일들(`test_assets_listing.py`, `test_social_integration.py` 등)의 이름을 변경하거나 폴더 구조를 정리하여 Pytest Collection Error를 해결하세요.
2. `Position` 모델이 제거되었으므로, 관련하여 깨지는 테스트나 잘못된 의존성이 남아있다면 코드를 수정하세요.
3. `TransactionService`에서 Buy/Sell 트랜잭션 발생 시 Computed Position이 정확하게 계산되는지 검증하는 통합 테스트를 추가 및 점검하세요.
4. 로컬에서 `pytest`를 실행하여 모든 테스트가 100% 통과하는지 확인하세요.

## 기대 산출물 (Expected Outputs)
- Pytest Collection Error가 해결된 깔끔한 테스트 폴더 구조.
- `pytest`가 실패 없이 모두 통과 (`tests/` 폴더 내 모든 테스트 성공).

## 참고 자료 (References)
- `.agent/project/artifacts/architecture/inspection_report_20260221.md`
