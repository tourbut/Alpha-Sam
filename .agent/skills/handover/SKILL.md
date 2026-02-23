---
name: handover
description: Handovers 완료 처리 규칙을 설명합니다. "Handovers", "완료 처리", "역할 이관" 등의 키워드가 언급되면 이 스킬을 고려.
---

## Purpose

역할(Role)별 Handovers(업무 이관) 작업이 완료되었을 때 이를 처리하고 로그를 남기는 규칙을 정의합니다.

## When to Run

- 역할별 할당 문서(`to_<role>.md`)에 적힌 모든 태스크(Tasks)를 완료했다고 판단될 때
- "Handovers", "완료 처리", "역할 이관" 등이 요청될 때

## Workflow

당신이 담당하는 Handovers 파일(`to_<role>.md`)에 적힌 **모든 Tasks를 완료했다고 판단되면**, 다음 단계를 수행해야 합니다.

1. **현재 Handovers 내용 이관 (날짜 기준, append 방식)**
   - 오늘 날짜 기준으로 다음 경로에 로그 파일을 기록합니다.
   `.agent/handovers/logs/YYYY-MM-DD_<role>.md`
   - 예: 백엔드 개발자의 경우
     `.agent/handovers/logs/2025-12-07_backend_dev.md`
2. 만약 해당 파일이 **이미 존재한다면**, 기존 내용을 삭제하지 않고 **현재 `to_<role>.md`의 내용을 아래에 append(추가 기록)** 합니다.
3. 만약 해당 파일이 **없다면**, 새로 생성한 뒤 `to_<role>.md`의 전체 내용을 기록합니다.
4. 이관이 끝난 후에는, `to_<role>.md` 내용을 전부 지워 다음 요청을 대기 상태로 만듭니다.

## Related Files

| File | Purpose |
|------|---------|
| `.agent/handovers/to_*.md` | 각 역할별로 진행할 작업 목록이 담긴 파일 |
| `.agent/handovers/logs/*.md` | 역할별 작업 완료 로깅 파일 (히스토리 보관용) |