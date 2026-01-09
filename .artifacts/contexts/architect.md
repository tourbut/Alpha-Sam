# Architect Context

## 1. Domain Model & Schema Alignment
*`domain_rules.md`에 정의된 핵심 도메인 개념을 기반으로 설계를 관리합니다.*

### Core Entities
- **Asset (자산)**
  - **정의**: 비트코인, 애플 주식 등 투자 대상.
  - **Schema**: `Asset` (Global vs Custom)
  - **Constraint**: `symbol`은 고유해야 함. `owner_id`가 NULL이면 전역 자산, 존재하면 개인화된 자산.
- **Position (보유 내역)**
  - **정의**: 특정 자산의 보유 상태 (수량, 평단가).
  - **Schema**: `Position`
  - **Rule**: `quantity >= 0`. `owner_id` 필수 (Multi-tenancy). (User, Asset) 조합의 Uniqueness 보장 필요.
- **Transaction (거래 이력)**
  - **정의**: 매수/매도 행위 기록.
  - **Schema**: `Transaction`
  - **Rule**: 이력 추가 시 `Position` 재계산(수량/평단가) 로직과 트랜잭션 단위로 묶여야 함.
- **Price (시세)**
  - **정의**: 시점별 자산의 현재 가치.
  - **Flow**: 외부 API -> Redis Cache -> DB (History) -> Client.

## 2. System Architecture (v0.7.0)
*See `tech_stack.md`*

### Backend
- **Framework**: FastAPI + SQLAlchemy (Async)
- **Multi-tenancy Strategy**:
  - **Type**: Row-Level Security (Logical Separation).
  - **Implementation**: 모든 Query/Command에서 `owner_id` 필터링 강제.
  - **Why**: 초기 단계에서 물리적 분리(Schema per user)보다 개발 속도와 관리 용이성이 높음(KISS).
- **Notification System**:
  - **Stack**: Celery + Redis
  - **Flow**: Price Update -> Check Alert Condition -> Enqueue Task -> Helper Service (SMTP) -> User Email.
  - **Why**: 이메일 발송은 Latency가 높으므로 메인 Request-Response 사이클에서 분리(Async).

### Frontend
- **Stack**: SvelteKit + TailwindCSS
- **State**: User Session 및 Settings 상태 관리.

## 3. Design Decisions & Rationale
*설계 결정의 근거(Why)를 기록합니다. 모든 기록은 `[YYYY-MM-DD HH:mm:ss]` 타임스탬프를 포함합니다.*

- [2025-12-20 11:30:00] **`owner_id` Migration Strategy**
    - **Decision**: 기존 데이터(`owner_id`=NULL)를 Default Admin 계정 소유로 일괄 업데이트.
    - **Reason**: Nullable로 유지 시 조회 로직이 복잡해짐(`owner_id` IS NULL OR `owner_id` = current). 명시적 소유권 할당이 데이터 무결성에 유리.

- [2025-12-24 09:00:00] **Notification Settings as 1:1 Entity**
    - **Decision**: `User` 테이블에 컬럼을 추가하는 대신 `NotificationSettings` 테이블로 분리.
    - **Reason**: 알림 설정 항목(채널별, 로직별)이 늘어날 가능성이 높음. User 테이블의 비대화(Bloating) 방지 (Separation of Concerns).

- [2025-12-24 14:00:00] **Price Alert Rate Limiting**
    - **Decision**: Redis Key `alert:{user_id}:{asset_id}:{date}` 활용하여 1일 1회 제한.
    - **Reason**: 급격한 변동 장세에서 스팸성 알림 폭탄 방지 (User Experience).

## 4. Current Status & Roadmap

### v0.7.0 (Current): Multi-tenancy & Notifications
- [2025-12-17 14:00:00] DB Schema: `owner_id` 추가 및 마이그레이션.
- [2025-12-20 10:45:00] Backend Interface: `X-User-Id` Header 기반 시뮬레이션.
- [2025-12-20 12:00:00] Core Feature: 이메일 알림 발송 로직 구현 (SMTP/Celery).
- [2025-12-27 10:48:14] v0.7.0 기능 구현 및 QA 마무리. API 문서 및 컨텍스트 동기화 진행 중.
- [2025-12-30 14:00:00] v0.8.0 QA Complete: Critical Bugs Fixed & Verified. Ready for Deployment.
- [2025-12-31 16:00:00] v0.9.0 Migration Plan Verified. QA results confirmed successful dirty data migration.
- [2026-01-01 16:50:00] v0.9.0 Production Verification: DB Migration Success, but API Smoke Test blocked by env issue. release/v0.9.0 merged to main.

### v1.0.0 (Upcoming): Official Launch
- **Goal**: Full Stability, Dashboard Analytics (Charts), UI Polish.
- **Key Features**:
    - Portfolio Performance Charts (pnl history).
    - Landing Page & User Guide.
    - Production Infrastructure Hardening (HTTPS, Auto-restart).

### v0.8.0 (Next): Authentication
- **Task**: `X-User-Id` 제거 및 JWT Auth 도입.
- **Status**: Development & QA Complete.
- **Next**: Post-Deployment Verification.
- **Ref**: `v0.8.0_post_deployment_verification.md`

### Decisions
- [2025-12-27 22:10:00] **Adoption of FastAPI Users**
    - **Decision**: 직접 구현 대신 `fastapi-users` 라이브러리 채택.
    - **Reason**: 보안 모범 사례(Oauth2, Hashing)가 내장되어 있고, 소규모 팀에서 인증 로직 유지보수 비용을 최소화하기 위함.
    - **Ref**: `v0.8.0_implementation_plan.md`

## 5. Handovers
- [2025-12-27 10:45:00] **Architect -> Backend**: `owner_id` 누락 없는지 CRUD 코드 리뷰 강화 요청.
- [2025-12-27 10:45:00] **Architect -> Frontend**: API 호출 시 User Context 전달 방식(Header vs Token) 변경 대비.
- [2026-01-08 17:15:00] **Feature Merged**: `feature/enhanced-mock-chat` (Mock Chat Widget with history) merged into `develop`. QA Verified.
- [2026-01-09 15:15:00] **v1.1.0 Planning**: Drafted `v1.1.0_architecture_draft.md`. Defined Schema for Social (PortfolioShare, Leaderboard) and Automation (Bot, Alerts).
