# Domain Rules

## 1. Core Entities

### User (사용자)
- **Role**: 시스템 사용자.
- **Attributes**:
  - `email` (Unique, Required): 로그인 ID로 사용.
  - `hashed_password`: 암호화된 비밀번호.
  - `is_active`: 계정 활성화 여부.
  - `is_superuser`: 관리자 권한 여부.
  - `nickname`: 사용자 표시 이름 (Optional).
- **Rules**:
  - 이메일 인증이 완료된 사용자만 주요 기능을 사용할 수 있어야 함 (Future).
  - v0.8.0부터는 `FastAPI Users` 기반의 표준 User 모델을 준수.

### Asset (자산)
- **Role**: 투자 대상 (암호화폐, 주식 등).
- **Attributes**:
  - `symbol` (Unique within scope): 티커 (예: BTC, AAPL).
  - `name`: 자산 이름.
  - `category`: 자산 유형 (Crypto, Stock, etc.).
  - `owner_id` (Nullable):
    - `NULL`: 전역(Global) 자산. 모든 유저가 접근 가능.
    - `Value`: 커스텀(Custom) 자산. 해당 유저만 접근 가능.

### Portfolio (포트폴리오)
- **Role**: 자산 및 거래 내역을 그룹화하는 컨테이너.
- **Attributes**:
  - `owner_id`: 소유자 FK.
  - `name`: 포트폴리오 명칭 (예: "메인 계좌", "비상금").
- **Rules**:
  - 유저는 최소 1개의 기본 포트폴리오를 가져야 한다.
  - 모든 Position과 Transaction은 반드시 하나의 Portfolio에 귀속된다.

### Transaction (거래 내역)
- **Role**: 자산의 매수/매도 행위 기록. 포지션 산출의 근거 데이터(Source of Truth).
- **Attributes**:
  - `portfolio_id`: 귀속 포트폴리오.
  - `type`: 매수(BUY)/매도(SELL).
  - `quantity`: 수량.
  - `price`: 체결 단가.
- **Rules**:
  - Transaction 추가/수정/삭제 시 귀속된 Portfolio의 해당 Asset Position을 재계산해야 한다.

### Price (시세 데이터)
- **Role**: 자산의 현재 가치. 데이터베이스에 영구 저장하지 않고 캐시(Redis)에 일시 저장.
- **Attributes**:
    - `price:{SYMBOL}`: 최신 가격 (Float String).
- **Rules**:
    - 가격 데이터는 **Collector**에 의해서만 갱신(Write)된다.
    - API 서비스는 오직 **Read**만 수행한다 (CQRS Lite).
    - Cache Miss 시 실시간 조회를 시도하지 않고, 적절한 Fallback(Mock/Error)을 반환한다.


### Position (보유 내역 - Computed Snapshot)
- **Role**: Transaction 이력을 기반으로 계산된 "현재 보유 상태".
- **Attributes**:
  - `portfolio_id`: 귀속 포트폴리오.
  - `quantity`: 보유 수량.
  - `avg_price`: 평단가.
- **Rules**:
  - **Read-Only**: 사용자가 직접 수량을 수정할 수 없다. 오직 Transaction을 통해서만 변경된다.
  - **Constraint**: `(portfolio_id, asset_id)`는 유일해야 한다.
  - **Legacy Migration**: v1.2.0 이전 데이터는 "Default Portfolio" 생성 후 이동시킨다.

### NotificationSettings (알림 설정)
- **Role**: 사용자별 알림 수신 설정.
- **Attributes**:
  - `user_id`: 소유자 FK (1:1 관계).
  - `email_enabled`: 이메일 알림 수신 여부.
  - `daily_digest_time`: 일간 리포트 수신 시간.

## 2. Invariants & Business Logic

### Multi-Portfolio & Tenancy
- 모든 자산 관련 데이터(Position, Transaction)는 `Portfolio`를 통해 간접적으로 `User`와 연결된다 (`User -> Portfolio -> Transaction`).
- 조회 시 `portfolio_id`가 해당 유저 소유인지 검증 필수.
- **v0.8.0 Change**: `X-User-Id` 헤더 기반의 식별을 폐지하고, JWT Token의 `sub` 클레임을 신뢰한다.

### Authentication & Authorization
- **Authentication**: JWT (JSON Web Token) 기반.
- **Password**: Argon2 알고리즘 사용.
- **Session**: Stateless. Access Token 만료 시 Refresh flow(Optional) 또는 재로그인.

### Price Alert
- 동일 사용자의 동일 자산에 대한 시세 알림은 24시간 내 1회로 제한한다 (Redis Key 활용).

### Social Features (v1.1.0)

### UserFollow (팔로우)
- **Role**: 사용자 간의 구독 관계.
- **Attributes**:
  - `follower_id`: FK User.
  - `following_id`: FK User.
- **Rules**:
  - Self-follow 불가능.
  - 중복 Follow 불가능.

### PortfolioVisibility (포트폴리오 공유)
- **Role**: 포트폴리오의 공개 설정.
- **Attributes**:
  - `portfolio_id`: PK/FK.
  - `visibility`: ENUM(PRIVATE, PUBLIC, LINK_ONLY).
  - `access_token`: UUID (for LINK_ONLY).
- **Rules**:
  - `LINK_ONLY`의 경우 `access_token`이 일치해야 조회 허용.

### LeaderboardRank (리더보드 집계)
- **Role**: Celery 배치 작업을 통해 주기적으로 갱신되는 랭킹 스냅샷.
- **Attributes**:
  - `user_id`: FK User. 인덱스 적용.
  - `portfolio_id`: FK Portfolio. 대표 포트폴리오 (is_primary_for_leaderboard=True).
  - `period`: ENUM(DAILY, WEEKLY, ALL_TIME). 집계 기간.
  - `rank`: 순위 (1부터 시작).
  - `return_rate`: 수익률 (소수점, 예: 0.15 = 15%).
  - `total_value`: 총 평가금액 (선택).
  - `updated_at`: 갱신 시점.
- **Rules**:
  - (user_id, period) 조합은 유일해야 함.
  - Redis 캐싱 적용 (TTL 10분).
  - 매시간 Celery Beat에 의해 재계산.

