# Handovers: To Architect

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- 프로젝트의 기능 매뉴얼과 전체 서비스 설명 문서가 필요합니다.
- 사용자가 `.artifacts/docs`에 해당 문서를 작성해달라고 요청했습니다.

## 해야 할 일 (Tasks)
1. `.artifacts/docs/functional_manual.md` 파일 생성 (또는 적절한 이름).
   - [x] 작성 완료.
2. **전체 서비스 설명** 작성 (프로젝트 목적, 주요 가치).
   - [x] `functional_manual.md`에 포함.
3. **기능 매뉴얼** 작성.
   - [x] `functional_manual.md`에 포함.

## 기대 산출물 (Expected Outputs)
- `.artifacts/docs/functional_manual.md`

## 참고 자료 (References)
- `.artifacts/projects/context.md`
- `.artifacts/task.md`
- 구현된 소스 코드 및 기존 문서들

---

# Handovers: To Architect

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- `PriceService`가 Yahoo Finance API에 직접 의존하여 느리고 불안정합니다.
- Redis를 도입하여 읽기와 쓰기를 분리하는 아키텍처로 변경하기로 결정되었습니다.

## 해야 할 일 (Tasks)
1. **Redis 데이터 스키마 확정 및 문서화**:
    - Key: `price:{SYMBOL}` (예: `price:BTC-USD`, `price:AAPL`)
    - Value: `String` (Float 값의 문자열 표현)
    - TTL: 180초 (3분) 권장
    - [x] 완료: `.artifacts/projects/redis_schema.md` 생성, `domain_rules.md` 업데이트.
2. **데이터 흐름 정의**:
    - `Collector Script` -> `Yahoo Finance` -> `Redis`
    - `PriceService` -> `Redis` (Fallback 없음, Cache Miss시 Mock/Error 처리)
    - [x] 완료: `redis_schema.md`에 데이터 흐름 명시.

## 기대 산출물 (Expected Outputs)
- 아키텍처 문서 또는 스키마 정의 문서가 업데이트되거나, 개발팀에 명확한 가이드 제공. (이 파일 자체가 가이드 역할을 함)

## 참고 자료 (References)
- `backend/app/src/engine/price_service.py`
- `.artifacts/projects/domain_rules.md`
