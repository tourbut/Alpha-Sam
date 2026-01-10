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
# Handovers: To Frontend Developer

## 날짜
- 2026-01-09

## 현재 상황 (Context)
- v1.1.0 설계를 바탕으로 **Social Features**의 UI/UX 구현이 필요합니다.
- 백엔드 API가 개발 중이므로, Mock 데이터를 활용하여 UI를 먼저 완성합니다.

## 해야 할 일 (Tasks)
1. **Shared Portfolio Modal**:
   - 대시보드 내 "Share" 버튼 추가.
   - 모달 내 설정 옵션 구현: "금액 숨기기", "수익률만 공개" 등 (Toggle Switch).
   - 링크 복사 기능.
2. **Leaderboard Page (`/social/leaderboard`)**:
   - 라우트 생성: `src/routes/social/leaderboard/+page.svelte`.
   - 데이터 테이블 구현: `Rank`, `User`, `PnL %`, `Winning Rate` 컬럼.
   - 내 순위 하이라이트 표시 기능.
3. **Mock Integration**:
   - `src/mocks/handlers.ts` (또는 유사)에 리더보드 가상 응답 데이터 추가하여 테스트.

## 기대 산출물 (Expected Outputs)
- `ShareModal.svelte` 컴포넌트가 작동하는 영상/스크린샷.
- `/social/leaderboard` 페이지 진입 시 테이블 렌더링 확인.

## 참고 자료 (References)
- `.artifacts/projects/v1.1.0_architecture_draft.md`
# Handovers: To QA Tester

## 날짜
- 2026-01-09

## 현재 상황 (Context)
- v1.1.0 (Social & Automation) 개발이 시작되었습니다.
- 본격적인기능 테스트에 앞서, 기획서를 바탕으로 테스트 시나리오를 미리 정의해야 합니다.

## 해야 할 일 (Tasks)
1. **Test Plan 작성 (v1.1.0)**:
   - **Social**: 포트폴리오 공유 링크 접근 제어(공개/비공개), 리더보드 필터링 및 정렬 검증.
   - **Automation**: 알림 조건 트리거 테스트 시나리오 구상.
2. **Regression Test Criteria**:
   - 기존 기능(포트폴리오 조회, 인증)에 영향을 주지 않는지 점검할 항목 선별.

## 기대 산출물 (Expected Outputs)
- `.artifacts/projects/qa_reports/test_plan_v1.1.0.md` 파일 생성.

## 참고 자료 (References)
- `.artifacts/projects/v1.1.0_architecture_draft.md`
