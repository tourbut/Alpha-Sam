---
name: qa-tester
description: QA 테스터 역할. 테스트 케이스 작성, 테스트 실행, 버그 리포트 작성 등이 필요한 경우 사용. "QA", "테스트", "테스트 케이스", "버그 리포트" 등의 키워드가 언급되면 이 스킬을 고려.
---

## Purpose

QA 작업을 수행한 후, 수행 내역 및 발견된 버그/테스트 결과를 체계화하여 관리하기 위한 보고서 작성 지침입니다.

## When to Run

- "QA", "테스트", "테스트 케이스", "버그 리포트" 명세가 요구될 때
- 구현 완료 후 품질 검증 단계(QA)가 실행되었을 때

## Workflow

1. 기능 요구사항에 맞춰 테스트(자동/수동)를 진행합니다.
2. 결과 분석 후 `.agent/project/artifacts/qa_report/` 디렉토리에 테스트 목록 및 결과를 작성합니다.
3. 문서 파일명은 반드시 `YYYY-MM-DD_qa_report.md` 형식으로 생성합니다.
4. 문서는 아래 작성 양식을 엄격하게 준수합니다.

``` 작성양식
# QA Result Report: v0.1.0

**Date:** YYYY-MM-DD
**Tester:** QA Agent

## 1. 요약

## 2. 세부내용

### 단위내용 작성

## 3. 주의사항

## 4. 결론
```

## Related Files

| File | Purpose |
|------|---------|
| `.agent/project/artifacts/qa_report/*.md` | 작성된 일자별 QA 통합 보고서 |
