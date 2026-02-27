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
  1. **Admin Asset Management**: 관리자 전용 종목 관리 UI 및 API. (Completed)
  2. **Batch Price Collector**: Celery Beat 기반 1분 주기 시세 자동 수집.
  3. **System Asset Source of Truth**: `AdminAsset` 테이블을 통한 중앙화된 시세 관리. (Completed)

## ✅ v2.0.0: Architecture Redesign (Completed)
- **Status**: Deployed
- **Themes**: Scalability, Security, Data Integrity.
- **Key Achievements**:
  1. **UUID Transition**: 모든 ID 체계를 Integer에서 UUID v4로 전환 완료.
  2. **Portfolio-Asset Relationship**: `Asset`이 `Portfolio`에 직접 귀속되도록 스키마 재구성.
  3. **Data Migration**: 기존 데이터의 무결성을 유지하며 UUID 기반 전환 완료.

## 🚧 v2.1.0: User Settings & Dashboard Analytics (In Progress)
- **Status**: Planning -> Backend Implementation
- **Themes**: User Experience, Data Visualization.
- **Key Deliverables**:
  1. **User Settings**: 닉네임 변경 및 비밀번호 재설정 페이지 추가.
  2. **Dashboard Overview**: 포트폴리오 가치 추이(Line Chart) 및 자산 비중(Pie Chart) 제공.
  3. **Analytics API**: 런타임 계산 기반 자산 비중 파이 차트 및 시계열 라인 차트 API 구현.

## 🚧 v2.2.0: Agent-Centric Interface (Planning)
- **Status**: Planning
- **Themes**: AI Integration, Token Efficiency, Headless Control.
- **Key Deliverables**:
  1. **Agent Login Interface**: CSS 배제, 시맨틱 HTML 기반 초경량 `/agent/login` 진입점 마련.
  2. **API Specification Payload**: 로그인 성공 직후, 에이전트가 즉시 활용 가능한 필수 CRUD API의 JSON 직렬화 명세 렌더링.
  3. **Headless Access**: 프론트엔드 DOM 파싱 없이, 획득한 JWT 토큰을 바탕으로 직접 백엔드 API를 호출하는 100% 신뢰성 기반의 제어 환경 제공.
