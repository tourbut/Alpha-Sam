---
name: Release Manager
description: 주요 개발 완료 후 develop 브랜치를 main 브랜치로 병합하고 버전을 태깅(Release)하는 스킬입니다. "릴리즈", "배포", "main에 병합" 등의 키워드가 언급되면 이 스킬을 고려합니다.
---

# Release Manager Skill

이 스킬은 주요 기능 개발이 완료되었을 때 호출됩니다. 프로젝트의 버전 관리 전략(`git-rules.md`)에 따라 `develop` 브랜치의 변경 사항을 `main` 브랜치에 안전하게 반영하고 릴리즈 태그를 생성합니다.

## 주요 동작 흐름

1. **상태 확인 및 버전 결정**
   - 현재 브랜치 상태 및 최근 커밋 로그, 최신 태그(`git tag -l`)를 조회하여 릴리즈에 포함될 내용을 파악합니다.
   - Semantic Versioning (MAJOR.MINOR.PATCH) 규격에 맞추어 다음 버전을 결정합니다. (예: 버그 수정은 PATCH, 새로운 단위 기능은 MINOR)
   - 사용자에게 결정된 버전 이름과 포함될 주요 업데이트 요약을 제시하고 승인을 구합니다.

2. **병합 및 태깅 수행**
   버전이 확정되면 아래의 git 명령어들을 순차적으로 실행하여 병합합니다:
   ```bash
   git checkout main
   git merge develop -m "Merge branch 'develop' into main: <Release Summary>"
   git tag -a v<VERSION> -m "Release v<VERSION>: <Release Summary>"
   ```

3. **원격 저장소 반영 (선택적)**
   - `git remote -v` 로 연결된 origin이 있는지 확인하고, 필요 시 `git push origin main` 및 `git push origin v<VERSION>` 명령어를 통해 푸시합니다.

4. **작업 환경 복귀**
   - 모든 작업이 완료되면 `git checkout develop` 명령어로 다시 로컬 개발 브랜치로 되돌아옵니다.
   - 사용자에게 작업 완료 및 최종 릴리즈 버전을 보고합니다.

## 주의 사항
- 항상 배포 작업 전 오류나 미커밋된 파일이 없는지 확인하세요.
- 병합 과정에서 충돌이 발생하면 즉시 병합을 중단하거나 충돌을 해결한 후 사용자에게 알립니다.
