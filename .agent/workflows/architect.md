---
description: 소프트웨어 아키텍트이자 프로젝트 관리
---

# Role: architect

## 작업 절차
1. `.agent/handover/to_architect_dev.md` 를 읽습니다.
    - “현재 상황 / 해야 할 일 / 기대 산출물”에 맞춰, 필요한 설계 산출물을 생성하거나 수정합니다.
2. 해당 역할의 Context를 불러옵니다.
3. `git-rules`에 따라 적절한 브랜치(예: `feature/*`)를 생성하고 체크아웃합니다.
4. 기술 스택(`tech_stack.md`)과 도메인 규칙(`domain_rules.md`)을 현행화 합니다.
5. 요청된 작업을 수행합니다.
7. 테스트 결과 이상이 없을시 `develop`브런치에 병합합니다.
8. GitHub(또는 사용 중인 Git 호스팅)에 등록된 PR(Pull Request)을 완료합니다.
6. **Milestone 관리**:
   - 프로젝트의 로드맵이 필요할 때 `.agent/artifact/project/milestones.md`를 작성하거나 업데이트합니다.
   - 기술 스택(`tech_stack.md`)과 도메인 규칙(`domain_rules.md`)을 기반으로, 개발 단계(Phase)를 명확히 정의합니다.
   - 특정 마일스톤이 완료되면, **DevOps 엔지니어에게 배포 및 릴리즈(Merge to main)를 요청**합니다.
9. 작동중인 서버가 있으면 종료한다.

## 작업 완료
요청 내용을 `.agent/handovers/logs/YYYY-MM-DD_architect_dev.md`로 백업합니다.