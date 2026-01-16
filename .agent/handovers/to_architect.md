# Handovers: To Architect

## 날짜
- 2026-01-16

## 브랜치 (Version Control)
- `feature/social-v1.1.0-design`

## 현재 상황 (Context)
- v1.4.0 배포가 성공적으로 완료되었습니다.
- 이제 다음 주요 업데이트인 v1.1.0(Social Features)의 상세 설계가 필요합니다.
- `v1.1.0_design_draft.md`를 바탕으로 실제 구현을 위한 명세서 작성이 요구됩니다.

## 해야 할 일 (Tasks)
1. **Database Schema Refinement**:
   - `Portfolio` 테이블에 `visibility`, `share_token` 필드 추가를 위한 Alembic 마이그레이션 계획 수립.
   - `UserFollow`, `LeaderboardRank` 테이블 상세 스펙 정의.
2. **API Specification Completion**:
   - `v1.1.0_design_draft.md`에 명시된 소셜 API들의 Request/Response 스키마 정의.
3. **Leaderboard Algorithm Selection**:
   - 주간 수익률 산정 방식 및 Celery 배치 작업 주기 확정.

## 기대 산출물 (Expected Outputs)
- `.agent/project/artifacts/architecture/v1.1.0_detailed_spec.md`

## 참고 자료 (References)
- `.agent/project/artifacts/architecture/v1.1.0_design_draft.md`
- `.agent/project/artifacts/milestone/milestones.md`
