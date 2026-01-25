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

## ✅ v1.1.0: Social Features (Completed)
- **Date**: 2026-01-19
- **Themes**: Social, Automation.
- **Key Achievements**:
  - **Portfolio Sharing**: Private/Public/Link-only visibility 구현 완료.
  - **Leaderboard**: Redis 기반 실시간 랭킹 시스템 구축.
  - **Social Graph**: 팔로우/팔로잉 기능 통합.

## 🚧 v1.5.0: System Administration & Batch Operations (In Progress)
- **Status**: Planning
- **Themes**: Admin, Automation, Data Accuracy.
- **Key Deliverables**:
  1. **Admin Asset Management**: 관리자 전용 종목 관리 UI 및 API.
  2. **Batch Price Collector**: Celery Beat 기반 1분 주기 시세 자동 수집.
  3. **System Asset Source of Truth**: `AdminAsset` 테이블을 통한 중앙화된 시세 관리.

## 🚀 v2.0.0: Architecture Redesign (In Progress)
- **Status**: Planning
- **Themes**: Scalability, Security, Data Integrity.
- **Key Deliverables**:
  1. **UUID Transition**: 모든 ID 체계를 Integer에서 UUID v4로 전환.
  2. **Portfolio-Asset Relationship**: `Asset`이 `Portfolio`에 직접 귀속되도록 스키마 변경.
  3. **Data Migration**: 기존 데이터의 무결성을 유지하며 UUID로 변환하는 마이그레이션 수행.
