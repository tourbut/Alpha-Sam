# Handovers: To Backend Developer

## 날짜
- 2026-01-23

## 브랜치 (Version Control)
- `feature/dashboard-recent-activity`

## 현재 상황 (Context)
- 대시보드(Frontend)에 "Recent Activity" 섹션을 구현하려 합니다.
- 사용자의 모든 포트폴리오, 자산 추가, 트랜잭션 기록 중 가청 최근 5개 항목을 통합 조회하는 API가 필요합니다.

## 해야 할 일 (Tasks)
1. **Schema 정의**:
   - `ActivityType` (Enum): `PORTFOLIO_CREATED`, `ASSET_ADDED`, `TRANSACTION_EXECUTED` (또는 유사한 구분)
   - `ActivityItem` (Model): `id`, `type`, `title`, `description`, `timestamp`, `entity_id`, `portfolio_id`(Optional) 등을 포함.

2. **API Endpoint 구현 (`/api/v1/dashboard/activities`)**:
   - **Method**: GET
   - **Logic**:
     - 현재 로그인한 사용자의:
       1) 최근 생성된 **Portfolios** (Created At 기준)
       2) 최근 추가된 **Assets** (Created At 기준)
       3) 최근 실행된 **Transactions** (Executed At 기준)
     - 위 3가지를 각각 상위 5~10개씩 Fetch 후, Python에서 하나의 리스트로 통합.
     - 통합 리스트를 `timestamp` 내림차순 정렬.
     - 상위 **5개**만 슬라이싱하여 반환.
   
3. **Response Example**:
   ```json
   [
     {
       "type": "transaction",
       "title": "Buy BTC",
       "description": "Bought 0.1 BTC in Main Portfolio",
       "timestamp": "2026-01-23T14:30:00Z",
       "entity_id": "...",
       "portfolio_id": "..."
     },
     {
       "type": "portfolio_create",
       "title": "New Portfolio",
       "description": "Created 'Retirement' portfolio",
       "timestamp": "2026-01-22T10:00:00Z",
...
   ]
   ```

## 기대 산출물 (Expected Outputs)
- `GET /api/v1/dashboard/activities` 호출 시 최근 활동 5개가 JSON 리스트로 반환됨.
