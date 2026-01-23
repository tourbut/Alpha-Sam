# Handovers: To Frontend Developer

## 날짜
- 2026-01-23

## 브랜치 (Version Control)
- `feature/dashboard-recent-activity`

## 현재 상황 (Context)
- 대시보드의 "Recent Activity" 섹션(현재 Placeholder)을 실제 데이터로 연동해야 합니다.
- Backend에서 통합 API (`/api/v1/dashboard/activities`)를 개발 중입니다.

## 해야 할 일 (Tasks)
1. **API Client 추가**:
   - `$lib/apis/dashboard.ts` (신규) 또는 `portfolio.ts`에 `getRecentActivities()` 함수 추가.
   - Endpoint: `GET /api/v1/dashboard/activities`
   - Type 정의: `ActivityItem` 인터페이스 추가.

2. **Dashboard UI 수정 (`src/routes/+page.svelte`)**:
   - `Recent Activity` 카드 내부의 Placeholder 텍스트 제거.
   - `{#each}` 블록을 사용하여 활동 리스트 렌더링.
   - 각 활동 타입(`PORTFOLIO`, `ASSET`, `TRANSACTION`)별로 적절한 아이콘/텍스트 표시.
     - 예: Transaction -> 화살표 아이콘, Portfolio -> 가방 아이콘 등.
   - 데이터 로딩 중/에러/비어있음 상태 처리.

## 기대 산출물 (Expected Outputs)
- 대시보드 진입 시 "Recent Activity" 섹션에 실제 사용자의 최근 활동 5개가 리스트 형태로 표시됨.
