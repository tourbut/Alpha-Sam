---
description: devops 수행
---

# Role: devops

## 작업 절차
1. `.agent/handover/to_devops.md` 를 읽습니다.
2. 해당 역할의 Context를 불러옵니다.
3. `git-rules`에 따라 적절한 `develop` 에 브런치에서 테스트를 수행합니다.
4. 요청된 작업을 수행합니다.
5. 요청 범위 밖의 변경(새로운 기능 추가 등)은 사용자가 명시적으로 요구하지 않는 한 진행하지 않습니다.
6. **Release & Deployment 관리**:
   - Architect의 요청이 있거나 정기 배포 시점에, `develop` -> `release` -> `main` 브랜치 병합을 수행합니다.
   - `main` 브랜치 병합 시 반드시 **Git Tag**를 생성하고, 프로덕션 배포 파이프라인이 정상 작동하는지 확인합니다.
7. 작동중인 서버가 있으면 종료한다.

## 작업 완료
요청 내용을 `.agent/handovers/logs/YYYY-MM-DD_devops.md`로 백업합니다.