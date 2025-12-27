# Handovers: To Backend Developer

## 2025-12-16

## 현재 상황 (Context)
- v0.6.0 QA 결과, **Critical Blocker (500 Error on Core APIs)** 가 발생했습니다.
- Architect가 v0.7.0 기획(User Isolation, Email Notification)을 완료했으나, v0.6.0 수정이 우선입니다.

## 해야 할 일 (Tasks)
1. **[URGENT]** v0.6.0 Critical Issue 해결 (참고: `.artifacts/qa_reports/qa_result_v060.md`).
   - `/assets`, `/portfolio` 500 에러 원인 확인 및 수정.
   - DB Migration 상태 확인.
2. v0.6.0 이슈 해결 후, v0.7.0 구현 계획 검토 (`v0.7.0_implementation_plan.md`).
3. v0.7.0 초기 구현 (DB Schema 변경: `owner_id` 추가).

## 기대 산출물 (Expected Outputs)
- v0.6.0 Hotfix.
- v0.7.0 DB Migration Script.

---

## 2025-12-16 Complete
- **v0.6.0 Hotfix**: Added explicit timeout (5s) to `yfinance` call in `price_service.py` to prevent thread exhaustion/hanging. Verified with stress test.
- **v0.7.0 Schema**: Added `owner_id` to `Asset` and `PortfolioHistory` models.
- **Migration**: Generated and applied `94215eaa8bdb` (nullable columns).
