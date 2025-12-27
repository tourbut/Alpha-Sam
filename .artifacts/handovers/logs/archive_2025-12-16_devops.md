# DevOps Log - 2025-12-16

## From: 2025-12-15 Handover

### Context
- v0.5.0 Production 배포 완료.
- v0.6.0 QA 진행 중 (Market Data Service 추가에 따른 외부 통신 필요).

### Tasks & Results
1. **v0.6.0 배포 준비**:
   - **Docker Container Connectivity**: Verified `yfinance` inside `alpha-sam-celery-worker` container (which shares backend image/network) can access external internet.
     - `yfinance` version: 0.2.66
     - Connectivity check: Success (Fetched AAPL history).
   - **Staging Test Scripts**: Created `check_v060_market.py` for verifying Market Data API.
     - Location: `/Users/shin/MyDir/MyGit/Alpha-Sam/check_v060_market.py`
     - Status: Verified locally against `localhost:8000`.

### Additional Actions Taken
- **Bug Fix**: Found `market` router was not included in `backend/app/src/api.py`. Added it to expose `/api/v1/market` endpoints.

### Status
- Ready for Staging Deployment.
