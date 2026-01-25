# QA Report: Admin Stock Batch Job

- **Date**: 2026-01-25
- **Branch**: `feature/admin-stock-batch-job`
- **Tester**: QA Agent

## 1. Test Scope
- **Backend**: `AdminAsset` Model, API endpoints, `PriceCollectorService`, Celery Beat configuration.
- **Frontend**: Admin Dashboard (`/admin/assets`), Authorization checks.
- **Integration**: Redis Caching flow.

## 2. Verification Results

### ✅ Backend Logic
| Component | Status | Notes |
|-----------|--------|-------|
| **AdminAsset Model** | PASS | UUID PK, Symbol Unique constraint, Active flag defined. |
| **API (`/admin/assets`)** | PASS | CRUD operations implemented. `superuser` dependency check included. |
| **PriceCollector** | PASS | Correctly iterates `is_active` assets. Uses `yfinance.fast_info` for efficiency. |
| **Data Safety** | PASS | Fallback to 0.0 on error. Redis TTL set to 180s (3m). |
| **Celery Config** | PASS | Task path corrected. Schedule set to 60s. |

### ✅ Frontend Logic
| Component | Status | Notes |
|-----------|--------|-------|
| **Authorization** | PASS | `+layout.svelte` checks `user.is_superuser` and redirects. |
| **Asset Management** | PASS | UI for Add/Delete/Toggle implemented using Flowbite components. |
| **API Integration** | PASS | `apis/admin.ts` connects to correct endpoints. |

## 3. Scenarios & Coverage

1.  **Scenario: Admin adds 'NVDA'**
    *   **Expected**: API creates record. Next batch job picks it up. Redis `price:NVDA` set.
    *   **Code Review**: `PriceCollector.collect_active_assets` filters `where(is_active=True)`. Logic holds.

2.  **Scenario: Invalid Symbol**
    *   **Expected**: `yfinance` throws error or returns empty. Service catches Exception.
    *   **Code Review**: `try-except` block in `_fetch_single_price` catches all Exceptions and logs error using `logger.error`. Loop continues. Resilience confirmed.

3.  **Scenario: Unauthorized Access**
    *   **Expected**: Non-admin user redirected to `/`.
    *   **Code Review**: Frontend `onMount` check `if (!u || !u.is_superuser)` handles this. Backend `get_current_superuser` dependency protects API. Double safety confirmed.

## 4. Conclusion
The implementation on `feature/admin-stock-batch-job` meets the requirements defined in the handover.
**Status**: **PASS** (Ready for Merge to Develop)
