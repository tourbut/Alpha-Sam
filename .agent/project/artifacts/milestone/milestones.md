# Alpha-Sam Milestones

## ✅ v0.7.0: Multi-tenancy & Notifications
- **Date**: 2025-12-27
- **Key Features**:
  - `owner_id` based row-level security.
  - Email notifications for price alerts (Celery/Redis).

## ✅ v0.8.0: Authentication
- **Date**: 2025-12-30
- **Key Features**:
  - JWT Authentication (FastAPI Users).
  - Secure Login/Register UI.
  - Protected Routes.

## ✅ v0.9.0: Data Migration
- **Date**: 2025-12-31
- **Key Features**:
  - Legacy Data Migration (Assign NULL owners to Admin).
  - Portfolio N+1 Optimization.
  - Production Deployment Pipeline Test.

## ✅ v1.0.0: Official Launch (Completed)
- **Date**: 2026-01-03
- **Themes**: Analytics, Stability, UX.
- **Key Achievements**:
  - Full PnL Analytics & Portfolio Charts.
  - UI/UX Polish (Dark Mode, Responsive Navbar).
  - Production Deployment with Docker Compose (Nginx, Redis, Celery).
  - Hotfixes Applied: `v1.0.1` (Dependency), `v1.0.2` (Volume Config).

## ✅ v1.2.0: Multi-Portfolio Structure (Completed)
- **Date**: 2026-01-11
- **Key Achievements**:
  - **Multi-Portfolio Support**: Users can manage multiple portfolios.
  - **Transaction-Centric Model**: Position accuracy improved via transaction history.
  - **Dashboard Fix**: Resolved API routing issue causing 404/Loading freeze.
- **Status**: Deployed to Production.

## 🔮 v1.1.0: Social Features (In Progress)
- **Status**: Planning / Design
- **Themes**: Social, Automation.
- **Key Deliverables**:
  1. **Portfolio Sharing**: Private/Public/Link-only visibility.
  2. **Leaderboard**: Periodic ranking system.
  3. **Social Graph**: Follow/Following.
