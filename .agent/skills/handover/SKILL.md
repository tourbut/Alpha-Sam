---
name: handover
description: Handovers 완료 처리 규칙을 설명합니다. "Handovers", "완료 처리", "역할 이관" 등의 키워드가 언급되면 이 스킬을 고려.
---

## ✅ Handovers 완료 처리 규칙 (공통)

당신이 담당하는 Handovers 파일(`to_<role>.md`)에 적힌 **모든 Tasks를 완료했다고 판단되면**,  
다음 단계를 수행해야 합니다.

**현재 Handovers 내용 이관 (날짜 기준, append 방식)**  
- 오늘 날짜 기준으로 다음 경로에 로그 파일을 사용합니다.  
  `.agent/handovers/logs/YYYY-MM-DD_<role>.md`
  - 예: 백엔드 개발자의 경우  
    `.agent/handovers/logs/2025-12-07_backend_dev.md`
- 만약 해당 파일이 **이미 존재한다면**, 기존 내용을 삭제하지 않고 **현재 `to_<role>.md`의 내용을 아래에 append(추가 기록)** 합니다.
- 만약 해당 파일이 **없다면**, 새로 생성한 뒤 `to_<role>.md`의 전체 내용을 기록합니다.

이관이 끝난 후에는, `to_<role>.md`는 다음 요청을 위해 비워집니다.