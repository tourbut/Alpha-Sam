# Deployment & Migration Checklist - v1.2.0

## 1. Pre-Deployment
- [x] **Snapshot Backup**: Create a full backup of the production database (`pg_dump` or RDS snapshot).
- [x] **Verify Artifacts**: Ensure `backend` and `frontend` images tagged `v1.2.0` are pushed to the registry.
- [x] **Service Status**: Check that all services are healthy before starting.

## 2. Maintenance Mode
- [ ] (Optional) Enable maintenance page in Nginx to prevent writes during migration.

## 3. Database Migration
```bash
# Execute Alembic Migration
docker compose run --rm backend alembic upgrade head
```
- **Verification**:
    - Check logs for "Data Migration" query execution (creating default portfolios).
    - Verify `portfolios` table exists.
    - Verify `positions` and `transactions` have `portfolio_id` set (NOT NULL).

## 4. Rollback Plan
If migration fails:
1.  **Downgrade Schema**:
    ```bash
    docker compose run --rm backend alembic downgrade -1
    ```
    *Note: This might be risky if data was partially moved. Prefer Restore if data integrity is compromised.*
2.  **Restore Backup**:
    - Stop application containers.
    - Restore DB from pre-deployment snapshot.
    - Restart with previous version images (v1.0.3).

## 5. Deployment
- Update `docker-compose.yaml` (or k8s manifests) to use image tag `v1.2.0`.
- Redeploy services:
    ```bash
    docker compose up -d
    ```

## 6. Post-Deployment Verification
- [ ] Check Logs: `docker compose logs -f backend`
- [ ] Health Check: `curl https://api.alpha-sam.com/health` returns 200.
- [ ] Smoke Test:
    1.  Login.
    2.  Check Dashboard (Portfolio should be "Default Portfolio" or "Main").
    3.  Create a test transaction.
