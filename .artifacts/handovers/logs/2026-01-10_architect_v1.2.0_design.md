# Handovers: To Architect

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- `PriceService` 리팩토링이 완료되어 시세 데이터 파이프라인이 안정화되었습니다.
- 사용자와의 논의를 통해 **1) Transaction 기반의 포지션 관리**, **2) Multi-Portfolio(다중 포트폴리오) 지원**이 차기 핵심 구조변경 사항으로 결정되었습니다.
- 현재는 User가 Asset/Position을 직접 소유하는 구조입니다 (`User -- Position`).

## 해야 할 일 (Tasks)
1. **도메인 모델 재설계 (v1.2.0 Design)**:
    - `Portfolio` 엔티티 정의 (User와 1:N 관계).
    - `Position` 및 `Transaction`이 User가 아닌 `Portfolio`에 귀속되도록 관계 수정.
    - `Position`을 수기 입력 대상에서 제외하고, `Transaction`의 결과물(Computed/Snapshot)로 재정의.
2. **ERD 및 스키마 명세 업데이트**:
    - `.artifacts/projects/domain_rules.md` 업데이트.
    - 새로운 엔티티 관계도 (Mermaid ERD) 작성.
3. **마이그레이션 전략 수립**:
    - 기존 User 소유의 Position/Transaction 데이터를 "Default Portfolio"로 이관하는 마이그레이션 로직 설계.

## 기대 산출물 (Expected Outputs)
- `.artifacts/projects/domain_rules.md` (업데이트됨)
- `.artifacts/projects/v1.2.0_schema_design.md` (신규 작성: ERD 및 마이그레이션 계획 포함)

## 참고 자료 (References)
- `.artifacts/contexts/architect.md`
- `backend/app/src/models/user.py`, `portfolio_history.py`, `position.py`
