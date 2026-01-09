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
