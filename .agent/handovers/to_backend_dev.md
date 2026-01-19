# Handovers: To Backend Developer

## 날짜
- 2026-01-19

## 현재 상황 (Context)
- v1.1.0 Architecture Design이 `develop` 브랜치에 병합됨 (`.agent/project/artifacts/architecture/v1.1.0_design_draft.md`).
- Social Features (Follow, Share) 및 Data Integrity 강화가 핵심 목표.

## 해야 할 일 (Tasks)
1. **Schema Implementation**:
   - `UserFollow` 모델 구현 (M:N).
   - `PortfolioShare` 모델 또는 필드 확장 구현.
   - DB Migration 스크립트 작성 (Alembic).
2. **API Logic**:
   - Social API Endpoints (`/follow`, `/share`) 구현.
3. **Data Integrity Refactoring**:
   - `create_transaction` 로직에서 `Position` 업데이트가 원자적(Atomic)으로 이루어지도록 수정.
   - Design Draft의 "3.3 Implementation Guideline" 참조.

## 기대 산출물 (Expected Outputs)
- Updated Models & API Endpoints
- Migration Scripts
