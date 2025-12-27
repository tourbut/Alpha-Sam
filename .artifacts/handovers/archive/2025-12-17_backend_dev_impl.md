# Handovers: To Backend Developer

## 날짜
2025-12-17 (Phase 1 Start)

## 현재 상황 (Context)
v0.7.0 구현 계획이 승인되었습니다. 이제 **Phase 1: DB Schema Migration**을 시작합니다.
`Transaction`과 `Position` 모델에 `owner_id`를 추가하고, 기존 데이터를 Default User(ID=1)로 마이그레이션해야 합니다.

## 해야 할 일 (Tasks)
1. **모델 수정 (`transaction.py`, `position.py`)**:
   - `owner_id` 컬럼 추가 (ForeignKey).
   - `Position`에 Unique Constraint 추가.
2. **Alembic 마이그레이션 생성 및 적용**:
   - `alembic revision --autogenerate`
   - 생성된 파일 수정 (기존 데이터 `owner_id=1` 업데이트 로직 추가).
   - `alembic upgrade head` 실행.
3. **검증**:
   - DB에 컬럼이 잘 생성되었는지 확인.

(Phase 2 & 3 Added implicitly)
4. Email Service Setup.
5. Notification Logic Hook.
