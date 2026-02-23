# Handovers: To Frontend Dev

## 날짜
- 2026-02-22

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- v2.0.0 마이그레이션이 완료되었고, v2.1.0 (User Settings 및 Dashboard Analytics) 기능에 대한 UI/UX 작업이 백엔드와 함께 병렬로 진행될 수 있는 상태입니다. (Mock 데이터를 활용한 사전 작업 요망)
- 백엔드에서는 관련 데이터를 `PUT /api/v1/users/me/profile`, `PUT /api/v1/users/me/password` 및 `GET /api/v1/analytics/portfolio/{portfolio_id}/...` 엔드포인트를 통해 제공할 예정입니다.

## 해야 할 일 (Tasks)
1. **User Settings 페이지 (`/settings`) 구현**:
   - `ProfileForm` 컴포넌트 구현: 닉네임 수정 및 리더보드 공개 여부 Toggle 버튼
   - `PasswordChangeForm` 컴포넌트 구현: 기존 비밀번호 및 새 비밀번호 입력 (유효성 검사 적용)
2. **Dashboard Analytics 기능 연동 (`/` 메인 대시보드 컴포넌트)**:
   - `AssetAllocationChart`: 포트폴리오의 자산 비중을 보여주는 파이(Pie) 차트 구현 (Chart.js 등 라이브러리 검토 요망)
   - `PortfolioPerformanceChart`: 기간(`1W`, `1M`, `1Y` 등)별 가치 추이를 보여주는 라인(Line) 차트 구현
   - 백엔드 구현 완료 전까지 프론트 단에서 Mock 데이터를 사용하여 레이아웃 및 차트 렌더링 확인

## 기대 산출물 (Expected Outputs)
- User Settings (`/settings`) 페이지 및 폼 컴포넌트
- 대시보드 내 Asset Allocation & Performance 차트 컴포넌트
- 프론트엔드 스타일 규칙(`verify-frontend-style`) 통과

## 참고 자료 (References)
- `.agent/project/artifacts/architecture/v2.1.0_design_spec.md`
