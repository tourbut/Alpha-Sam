# Handovers: To DevOps

## 날짜
- 2026-01-13

## 현재 상황 (Context)
- 현재 활성 브랜치들이 작업 마무리 단계임.
- QA 및 프론트엔드 검증이 끝나면 모든 피처 브랜치를 `develop`으로 병합하고 삭제해야 함.

## 해야 할 일 (Tasks)
1. **Merge Preparation**
   - QA Sign-off 대기.
   - `develop` 브랜치 최신화 (`git checkout develop && git pull origin develop`).

2. **Final Merge Execution** (QA 승인 후 진행)
   - `feature/position-refactoring-qa-fixes` -> `develop` 병합 (Squash Merge 권장).
   - `feature/social-features` -> `develop` 병합 (Squash Merge 권장).
   - 충돌 발생 시 코디네이터/개발자와 상의하여 해결.

3. **Branch Cleanup**
   - 병합된 로컬/원격 브랜치 삭제.
     - `feature/position-refactoring-qa-fixes`
     - `feature/social-features`
     - 기타 `docs/*` 브랜치들도 내용 확인 후 병합 또는 삭제.
   - 최종적으로 `main`과 `develop` 브랜치만 남김.

## 기대 산출물 (Expected Outputs)
- `git branch -a` 조회 시 `main`, `develop` 만 존재.
- `develop` 브랜치에 모든 최신 변경사항 포함.
