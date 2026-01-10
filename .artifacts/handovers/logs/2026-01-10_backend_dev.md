# Handovers: To Backend Developer

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- **v1.2.0 아키텍처**로 전환합니다.
- 핵심 변경:
    1. `User`는 여러 `Portfolio`를 가짐.
    2. `Position`과 `Transaction`은 `Portfolio`에 귀속됨.
    3. `Position`은 `Transaction`의 결과물로 자동 계산됨 (더 이상 직접 수정 불가).

## 해야 할 일 (Tasks)
1. **DB Schema Migration**:
    - `Portfolio` 모델 생성 (`models/portfolio.py`).
    - `Position` 및 `Transaction` 모델 수정 (`portfolio_id` 추가, `owner_id` 제거/Deprecated).
    - `Alembic` 마이그레이션 스크립트 작성 (기존 데이터 -> Default Portfolio로 연결).
2. **API Implementation (Portfolio)**:
    - `POST /api/v1/portfolios`: 포트폴리오 생성.
    - `GET /api/v1/portfolios`: 목록 조회.
    - `GET /api/v1/portfolios/{id}`: 상세 조회.
3. **API Implementation (Transaction)**:
    - `POST /api/v1/portfolios/{id}/transactions`: 거래 내역 추가 (및 Position 자동 갱신 트리거).
    - `GET /api/v1/portfolios/{id}/transactions`: 거래 내역 조회.

## 기대 산출물 (Expected Outputs)
- `Portfolio` CRUD API 동작.
- 거래 내역 추가 시 `Position` 수량/평단가가 자동 계산되어 반영되는 로직 검증.

## 참고 자료 (References)
- `.artifacts/projects/v1.2.0_schema_design.md` (상세 명세)
- `.artifacts/projects/domain_rules.md`
