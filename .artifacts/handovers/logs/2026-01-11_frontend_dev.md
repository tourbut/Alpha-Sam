# Frontend Developer Work Log - 2026-01-11

## v1.2.0 Release Support
- Resolved merge conflicts in `frontend/src/routes` and documentation.
- Prioritized v1.2.0 logic (new transaction UI, multi-portfolio).

## Hotfix: v1.2.1 (Critical Import Error)
- **Incident**: QA Smoke Test failed with 500 Internal Error (Module not found).
- **Cause**: Refactor of `auth` store to Svelte 5 Runes (`auth.svelte.ts`) broke imports in `fastapi.js` and other files which were still looking for `$lib/stores/auth`.
- **Fix**:
    - Updated imports to `$lib/stores/auth.svelte` in:
        - `fastapi.js`
        - `routes/login`, `routes/signup`, `routes/transactions`, `routes/+page.svelte`
        - `Settings.test.ts`
        - `apis/auth.js`
    - Removed `$auth` store syntax (dollar sign) in Svelte components as `auth` is now a reactive class instance.
    - Updated `portfolio.ts` to include missing exports (`get_portfolio_history`, etc.) and deleted conflicting `portfolio.js`.
    - Fixed API usage in `transactions/+page.svelte` (object params for `getTransactions`).
- **Result**: Login page loads successfully. `v1.2.1` released.
