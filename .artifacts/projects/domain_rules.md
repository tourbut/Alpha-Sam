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

### Position (보유 내역)
- **Role**: 포트폴리오 내 특정 자산의 보유 상태.
- **Attributes**:
  - `quantity`: 보유 수량. 양수여야 함.
  - `avg_price`: 평단가.
- **Rules**:
  - `owner_id`는 필수 (Multi-tenancy).
  - 동일한 `owner_id` 하에서 `asset_id`는 유일해야 함.

### NotificationSettings (알림 설정)
- **Role**: 사용자별 알림 수신 설정.
- **Attributes**:
  - `user_id`: 소유자 FK (1:1 관계).
  - `email_enabled`: 이메일 알림 수신 여부.
  - `daily_digest_time`: 일간 리포트 수신 시간.

## 2. Invariants & Business Logic

### Multi-tenancy
- 모든 개인화 리소스(Position, Transaction, NotificationSettings)는 `owner_id`를 가져야 한다.
- DB 쿼리 시 반드시 `owner_id` 필터링을 수행하여 타 사용자의 데이터 접근을 원천 차단한다.
- **v0.8.0 Change**: `X-User-Id` 헤더 기반의 식별을 폐지하고, JWT Token의 `sub` 클레임을 신뢰한다.

### Authentication & Authorization
- **Authentication**: JWT (JSON Web Token) 기반.
- **Password**: Argon2 알고리즘 사용.
- **Session**: Stateless. Access Token 만료 시 Refresh flow(Optional) 또는 재로그인.

### Price Alert
- 동일 사용자의 동일 자산에 대한 시세 알림은 24시간 내 1회로 제한한다 (Redis Key 활용).
