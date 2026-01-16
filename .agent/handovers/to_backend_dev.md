# Handovers: To Backend Developer

## 날짜
- 2026-01-16

## 브랜치 (Version Control)
- `feature/social-v1.1.0-backend`

## 현재 상황 (Context)
- v1.4.0 릴리즈가 완료되었으며, 백엔드 버전이 1.4.0으로 업데이트되었습니다.
- v1.1.0 소셜 기능 구현을 시작합니다.
- 첫 단계로 포트폴리오 공유 기능(Portfolio Sharing)을 개발해야 합니다.

## 해야 할 일 (Tasks)
1. **Database Migration**:
   - `Portfolio` 모델에 `visibility` (Enum: PRIVATE, PUBLIC, LINK_ONLY) 및 `share_token` (UUID) 필드 추가.
2. **Visibility API Implementation**:
   - `PATCH /api/v1/portfolios/{id}/visibility` 엔드포인트 구현.
3. **Shared Portfolio Access**:
   - `GET /api/v1/portfolios/shared/{token}` 엔드포인트 구현 (비로그인 사용자도 접근 가능해야 함).

## 기대 산출물 (Expected Outputs)
- Alembic migration script
- Updated Portfolio Model & CRUD logic
- New Social API router

## 참고 자료 (References)
- `.agent/project/artifacts/architecture/v1.1.0_design_draft.md`
