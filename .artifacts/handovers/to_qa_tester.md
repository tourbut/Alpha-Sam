# Handovers: To QA Tester

## 날짜
- 2026-01-13

## 현재 상황 (Context)
- `feature/position-refactoring-qa-fixes`: 포지션 리팩토링 관련 QA 수정사항 반영 중.
- `feature/social-features`: 소셜 기능(Phase 1) 구현 상태.
- **최종 목표**: 모든 브랜치를 `develop`에 병합하고, `main`과 `develop`만 남기는 것.

## 해야 할 일 (Tasks)
1. **`feature/position-refactoring-qa-fixes` 검증**
   - 로컬에서 해당 브랜치 체크아웃.
   - 포지션 관련 기능(트랜잭션 추가/포트폴리오 계산) 정상 동작 확인.
   - 워크플로우 수정 사항(GitHub Actions 등) 확인.
   
2. **`feature/social-features` (Phase 1) 검증**
   - 로컬에서 해당 브랜치 체크아웃.
   - 공유하기 모달, 리더보드 UI 렌더링 확인 (Mock 데이터 기준).
   - 빌드/테스트 에러 없는지 확인.

3. **최종 Sign-off**
   - 두 기능 모두 `develop` 병합 가능한 수준인지 판단 후 리포트 작성 (`qa_reports/final_merge_check.md`).

## 기대 산출물 (Expected Outputs)
- `.artifacts/projects/qa_reports/final_merge_check.md` (병합 승인 여부 포함)
