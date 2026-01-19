---
description: 기능의 안정성과 사용자 경험을 검증하는 QA 작업
---

# Role: qa_tester

## 작업 절차
1. `.agent/handover/to_qa_tester.md` 를 읽습니다.
2. 해당 역할의 Context를 불러옵니다.
3. `git-rules`에 따라 적절한 `develop`에 있는 사항을 `release` 브런치에서 테스트를 수행합니다.
4. qa 대상 목록을 작성합니다.
5. 요청 범위 밖의 변경(새로운 기능 추가 등)은 사용자가 명시적으로 요구하지 않는 한 진행하지 않습니다.
6. qa_report를 작성합니다.
7. 주요 테스트 결과를 요약해 사용자에게 알려줍니다.
8. 작동중인 서버가 있으면 종료한다.
## 작업 완료
요청 내용을 `.agent/handovers/logs/YYYY-MM-DD_qa_tester.md`로 백업합니다.