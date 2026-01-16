---
description: 새로운 백엔드 작업을 시작할 때 사용하는 워크플로우
---

당신은 지금부터 `.agent/skills/backend-dev/SKILL.md`에 정의된
`backend-dev` 스킬을 사용해서 작업해야 한다.

1. `.artifacts/handovers/to_backend_dev.md`를 읽어 현재 백엔드 작업 요청을 파악한다.
2. `backend-dev` 스킬을 로드하고, 그 안의 지침과 핸드오버 규칙을 따르며 작업을 진행한다.
3. 작업을 진행하면서 필요한 컨텍스트는 `.artifacts/contexts/backend_dev.md`에서 로드하고, 새로운 결정/교훈은 거기에 축적한다.
4. 모든 Tasks를 완료했다고 판단되면, `backend-dev` 스킬에 정의된 Handovers 완료 규칙에 따라 로그 파일을 갱신하고, `to_backend_dev.md`를 비운다.