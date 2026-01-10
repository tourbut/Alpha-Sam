# Handovers: To Backend Developer

## 날짜
- 2026-01-09

## 현재 상황 (Context)
- v1.1.0 (Social & Automation) 설계 초안이 승인되었습니다.
- **Phase 1: Social Features** 구현을 시작합니다. 아키텍처에 따라 Leaderboard는 Redis를 캐시/스토리지로 활용해야 합니다.

## 해야 할 일 (Tasks)
1. **DB Schema Implementation**:
   - `PortfolioShare` 테이블 생성. (`user_id`, `settings` JSON, `is_active` BOOL).
   - `UserProfile` 모델 확장 및 `is_public_leaderboard` 필드 추가.
   - Alembic 마이그레이션 스크립트 작성 및 적용.
2. **Redis Integration (Leaderboard)**:
   - Leaderboard 점수(PnL%)를 저장하기 위한 Redis Sorted Set 구조 설계 (`leaderboard:weekly`).
   - (Optional) 백그라운드 PnL 계산 로직의 스켈레톤 코드 작성.
3. **API Implementation**:
   - `POST /portfolio/share`: 공유 링크 생성 (UUID 반환).
   - `GET /social/leaderboard`: Redis에서 Top N 조회하여 반환하는 엔드포인트.

## 기대 산출물 (Expected Outputs)
- 마이그레이션 파일.
- `app/src/routes/social.py` (신규 라우터).
- 로컬 환경에서 `/social/leaderboard` 호출 시 Mock 데이터 또는 빈 리스트 응답 확인.

## 참고 자료 (References)
- `.artifacts/projects/v1.1.0_architecture_draft.md` (Social Features 섹션)
