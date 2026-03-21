---
description: 최종 작업 브랜치를 develop 및 main에 순차적으로 병합
---

# 병합 워크플로우 (Release / Merge to Main)

현재 활성화되어 있는 작업 브랜치의 변경 사항을 최종으로 `develop`과 `main` 브랜치까지 순차적으로 병합하여 프로젝트를 최신화하는 절차입니다.

아래 단계를 순차적으로 실행하세요 (토큰 낭비를 최소화하기 위해 간결하게 실행 상황만 보고하세요):

1. 커밋 상태 확인
- `git status`로 현재 브랜치에 커밋되지 않은 변경 사항이 있는지 확인합니다.
- 변경 사항이 남아 있다면 모두 commit 처리합니다.

2. 원격 동기화
- `git fetch origin`

3. `develop` 브랜치 병합 (작업 브랜치가 develop이 아닌 경우)
- `git checkout develop`
- `git pull origin develop`
- `git merge <원래_작업_브랜치>`
- `git push origin develop`

4. `main` 브랜치 병합
- `git checkout main`
- `git pull origin main`
- `git merge develop`
- `git push origin main`

5. 마무리
- `git checkout develop` (작업 기반 브랜치로 복귀) 
- 필요할 경우 사용자에게 병합이 완료된 이전 작업 브랜치의 삭제 여부를 문의합니다.
