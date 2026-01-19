---
description: frontend_dev 수행
---

# Role: frontend_dev

## 작업 절차
1. `.agent/handover/to_frontend_dev.md` 를 읽습니다.
    - 현재 어떤 브랜치/파일/기능을 대상으로 작업해야 하는지,
    - 어떤 변경이 필요한지,
    - 어떤 산출물이 기대되는지 파악합니다.
2. 해당 역할의 Context를 불러옵니다.
3. `git-rules`에 따라 적절한 브랜치(예: `feature/*`)를 생성하고 체크아웃합니다.
4. GitHub(또는 사용 중인 Git 호스팅)에서 PR(Pull Request)을 생성합니다.
5. 개발 요청사항을 수행합니다.
    - 요청 범위 밖의 변경(새로운 기능 추가 등)은 사용자가 명시적으로 요구하지 않는 한 진행하지 않습니다.
6. 단위 테스트를 수행합니다.
7. 테스트 결과 이상이 없을시 `develop`브런치에 병합합니다.
8. GitHub(또는 사용 중인 Git 호스팅)에 등록된 PR(Pull Request)을 완료합니다.
9. 변경된 주요 파일과 핵심 변경 내용을 요약해 사용자에게 알려줍니다.
10. 작동중인 서버가 있으면 종료한다.

## 작업 완료
요청 내용을 `.agent/handovers/logs/YYYY-MM-DD_frontend_dev.md`로 백업합니다.