# QA Verification Checklist v0.9.0
> **Target Release**: v0.9.0 (Data Migration)
> **Date**: 2025-12-31

## 1. Migration Verification
- [x] **Data Integrity**: 
  - [x] All `Asset` records must have a valid `owner_id` (unless explicitly allowed as NULL by new rules).
  - [x] Check if `Asset` ID=11 (Legacy Test Coin) has been migrated or handled (e.g., assigned to a default admin or deleted).
  - [x] `Position` records must link to valid `User` and `Asset`.

## 2. Regression Testing (Core)
- [ ] **Login/Auth**:
  - [ ] Login with existing user.
  - [ ] `/users/me` returns correct profile.
- [ ] **Portfolio**:
  - [ ] View Portfolio lists correctly.
  - [ ] Add new asset (updates `owner_id` correctly).
  - [ ] Edit/Delete asset.

## 3. Dirty Data Check (Pre-Migration)
*Ensure these exist before running migration scripts*
- [x] Orphaned Asset (Symbol: LEGACY, ID: 11) - Created by `scripts/qa_generate_dirty_data_v090.py`
