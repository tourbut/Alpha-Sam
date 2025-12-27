# Position 모델 설계 문서

## 작성일
2025-12-07

## 개요
Alpha-Sam 프로젝트에서 사용자의 자산 보유 내역(Position/Holding)을 관리하기 위한 데이터베이스 스키마 및 아키텍처 설계 문서입니다.

---

## 1. Position 모델 스키마 설계

### 1.1 테이블 구조

**테이블명**: `positions`

| 필드명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 고유 ID |
| `asset_id` | INTEGER | NOT NULL, FOREIGN KEY → assets.id, UNIQUE | Asset 참조 (1:1 관계) |
| `quantity` | NUMERIC(20, 8) | NOT NULL, CHECK (quantity >= 0) | 보유 수량 (0 이상) |
| `buy_price` | NUMERIC(20, 8) | NOT NULL, CHECK (buy_price > 0) | 매수 단가 (0 초과) |
| `buy_date` | DATE | NULL | 매수 일자 (선택적) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | 레코드 생성 시각 |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NULL, ON UPDATE now() | 레코드 수정 시각 |

### 1.2 인덱스 설계

- **Primary Key**: `id`
- **Foreign Key Index**: `asset_id` (UNIQUE 제약으로 1:1 관계 보장)
- **추가 인덱스**: 필요 시 `buy_date`에 인덱스 추가 고려 (매수 일자 기준 조회가 빈번한 경우)

### 1.3 제약조건

1. **UNIQUE 제약**: `asset_id`에 UNIQUE 제약을 걸어 한 Asset당 하나의 Position만 허용
2. **CHECK 제약**: 
   - `quantity >= 0`: 보유 수량은 0 이상
   - `buy_price > 0`: 매수 단가는 0 초과
3. **Foreign Key**: `asset_id`는 `assets.id`를 참조하며, CASCADE 삭제 정책은 비즈니스 요구사항에 따라 결정
   - 권장: `ON DELETE CASCADE` (Asset 삭제 시 Position도 함께 삭제)

---

## 2. Asset-Position 관계 정의

### 2.1 관계 유형

**1:1 관계 (One-to-One)**

- 한 Asset당 **정확히 하나의 Position**만 존재할 수 있습니다.
- 이는 일반적인 자산 관리 시나리오에 부합합니다:
  - 사용자는 특정 자산(예: BTC)에 대해 하나의 보유 내역만 관리
  - 여러 번 매수한 경우에도, 평균 매수 단가와 총 수량으로 통합 관리

### 2.2 관계 구현 방법

#### SQLModel 모델 레벨
```python
# Asset 모델에 추가
position: Optional["Position"] = Relationship(back_populates="asset")

# Position 모델에 추가
asset: Optional["Asset"] = Relationship(back_populates="position")
```

#### 데이터베이스 레벨
- `positions.asset_id`에 **UNIQUE 제약**을 추가하여 데이터베이스 레벨에서 1:1 관계를 보장

### 2.3 관계의 장점

1. **단순성**: 복잡한 집계 로직 없이 Asset과 Position을 직접 조인 가능
2. **일관성**: 한 Asset에 대한 보유 정보가 항상 하나로 명확
3. **성능**: JOIN 쿼리가 단순하고 효율적

### 2.4 대안 고려사항

만약 향후 "여러 번 매수한 내역을 개별적으로 추적"해야 하는 요구사항이 생긴다면:
- `positions` 테이블에서 `asset_id`의 UNIQUE 제약을 제거
- `buy_transactions` 같은 별도 테이블을 도입하여 매수 이력을 관리
- 현재는 **1:1 관계로 시작**하고, 필요 시 확장하는 전략을 권장

---

## 3. 수익률 계산 로직 위치 결정

### 3.1 결정: 백엔드에서 계산

**수익률 계산 로직은 백엔드 API에서 수행**합니다.

### 3.2 결정 근거

1. **일관성 보장**
   - 여러 클라이언트(웹, 모바일 등)에서 동일한 계산 로직 사용
   - 계산 규칙 변경 시 백엔드만 수정하면 됨

2. **데이터 정합성**
   - 현재 시세(Price)와 보유 내역(Position)을 함께 조회하여 계산
   - 시세가 없는 경우 등 에지 케이스를 백엔드에서 일관되게 처리

3. **성능 최적화**
   - 데이터베이스에서 JOIN 및 집계 연산 수행 가능
   - 프론트엔드에서 불필요한 계산 부하 제거

4. **보안**
   - 민감한 계산 로직을 클라이언트에 노출하지 않음

### 3.3 계산 로직 위치

#### API 엔드포인트 레벨
- `GET /api/assets/{asset_id}` 또는 `GET /api/assets/{asset_id}/summary`
  - 단일 자산의 평가액, 손익, 수익률 반환

- `GET /api/portfolio/summary`
  - 전체 포트폴리오의 총 평가액, 총 손익, 포트폴리오 수익률 반환

#### 서비스 레벨 (권장)
- `app/services/portfolio_service.py` 또는 `app/services/position_service.py`에 계산 로직 구현
- 재사용 가능한 함수로 분리:
  ```python
  async def calculate_position_metrics(
      position: Position,
      current_price: Optional[Price]
  ) -> PositionMetrics:
      """
      단일 포지션의 평가액, 손익, 수익률 계산
      """
      pass
  
  async def calculate_portfolio_summary(
      positions: List[Position],
      prices: Dict[int, Price]
  ) -> PortfolioSummary:
      """
      전체 포트폴리오의 집계 계산
      """
      pass
  ```

### 3.4 계산 규칙 (domain_rules.md 참조)

#### 단일 포지션
- **평가액**: `current_price * quantity`
- **손익**: `(current_price - buy_price) * quantity`
- **수익률 (%)**: `((current_price - buy_price) / buy_price) * 100`

#### 전체 포트폴리오
- **총 평가액**: 모든 포지션의 평가액 합
- **총 손익**: 모든 포지션의 손익 합
- **포트폴리오 수익률**: 원금 가중 수익률
  - `total_invested = Σ (buy_price * quantity)`
  - `total_valuation = Σ (current_price * quantity)`
  - `portfolio_return_rate = ((total_valuation - total_invested) / total_invested) * 100`

### 3.5 에지 케이스 처리

1. **시세가 없는 경우**
   - `current_price`가 `None`이면 평가액, 손익, 수익률을 계산하지 않음
   - API 응답에 `"price_unavailable": true` 플래그 포함

2. **0으로 나누기 방지**
   - `buy_price == 0`인 경우 수익률 계산하지 않음
   - 데이터베이스 CHECK 제약으로 이미 방지되지만, 코드 레벨에서도 검증

3. **quantity == 0인 경우**
   - 평가액과 손익은 0으로 계산
   - 수익률은 계산하지 않거나 "보유 없음" 상태로 표시

---

## 4. Alembic 마이그레이션 가이드

### 4.1 마이그레이션 파일 생성

```bash
cd backend
alembic revision --autogenerate -m "add_position_model"
```

### 4.2 예상되는 마이그레이션 내용

```python
def upgrade() -> None:
    # positions 테이블 생성
    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('buy_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('buy_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], 
                               ondelete='CASCADE'),
        sa.CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        sa.CheckConstraint('buy_price > 0', name='check_buy_price_positive'),
    )
    
    # UNIQUE 제약 추가 (1:1 관계 보장)
    op.create_unique_constraint('uq_positions_asset_id', 'positions', ['asset_id'])
    
    # 인덱스 추가
    op.create_index(op.f('ix_positions_asset_id'), 'positions', ['asset_id'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_positions_asset_id'), table_name='positions')
    op.drop_table('positions')
```

### 4.3 마이그레이션 실행

```bash
# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백 (필요 시)
alembic downgrade -1
```

### 4.4 주의사항

1. **기존 데이터 마이그레이션**
   - 기존에 Asset 데이터가 있다면, Position 데이터를 어떻게 생성할지 결정 필요
   - 수동으로 Position을 생성하거나, 기본값으로 Position을 자동 생성하는 스크립트 작성 고려

2. **외래키 제약**
   - `ON DELETE CASCADE` 정책은 Asset 삭제 시 Position도 함께 삭제됨
   - 비즈니스 요구사항에 따라 `RESTRICT` 또는 `SET NULL`로 변경 가능

---

## 5. 다음 단계 (백엔드 개발자에게 전달)

### 5.1 구현 순서

1. **Position 모델 생성**
   - `backend/app/models/position.py` 파일 생성
   - SQLModel 기반 모델 정의 (Asset, Price 모델 참고)

2. **모델 관계 설정**
   - `Asset` 모델에 `position` 관계 추가
   - `Position` 모델에 `asset` 관계 추가
   - `backend/app/models/__init__.py`에 Position 모델 export

3. **Alembic 마이그레이션**
   - `alembic revision --autogenerate` 실행
   - 생성된 마이그레이션 파일 검토 및 수정
   - `alembic upgrade head` 실행

4. **Pydantic 스키마 생성**
   - `backend/app/schemas/position.py` 파일 생성
   - Position 생성/수정/조회용 스키마 정의

5. **API 엔드포인트 구현**
   - `backend/app/api/endpoints/positions.py` 파일 생성
   - CRUD 엔드포인트 구현:
     - `POST /api/positions` - Position 생성
     - `GET /api/positions/{position_id}` - Position 조회
     - `PUT /api/positions/{position_id}` - Position 수정
     - `DELETE /api/positions/{position_id}` - Position 삭제
     - `GET /api/positions` - Position 목록 조회

6. **수익률 계산 서비스 구현**
   - `backend/app/services/portfolio_service.py` 파일 생성
   - 단일 포지션 및 포트폴리오 집계 계산 로직 구현

7. **통합 API 엔드포인트**
   - `GET /api/assets/{asset_id}/summary` - 자산별 평가액/수익률 조회
   - `GET /api/portfolio/summary` - 전체 포트폴리오 요약

### 5.2 참고 파일

- 기존 모델: `backend/app/models/asset.py`, `backend/app/models/price.py`
- 기존 API: `backend/app/api/endpoints/assets.py`
- 기존 스키마: `backend/app/schemas/asset.py`

---

## 6. 설계 결정 요약

| 항목 | 결정 사항 | 근거 |
|------|----------|------|
| **관계 유형** | Asset : Position = 1:1 | 단순성, 일관성, 성능 |
| **UNIQUE 제약** | `asset_id`에 UNIQUE 적용 | 1:1 관계 보장 |
| **수익률 계산 위치** | 백엔드 API | 일관성, 정합성, 보안 |
| **계산 로직 위치** | 서비스 레이어 (`portfolio_service.py`) | 재사용성, 테스트 용이성 |
| **에지 케이스 처리** | 백엔드에서 명시적 처리 | 일관된 사용자 경험 |

---

## 7. 향후 확장 고려사항

1. **다중 매수 내역 추적**
   - 현재는 1:1 관계로 시작하되, 향후 `buy_transactions` 테이블 도입 고려

2. **매도 내역 관리**
   - 현재는 매수 정보만 관리하지만, 향후 매도 내역을 별도 테이블로 관리 가능

3. **수익률 계산 방식 확장**
   - 현재는 단순 수익률만 계산하지만, 시간 가중 수익률(IRR) 등 추가 가능

4. **히스토리 추적**
   - Position 변경 이력을 별도 테이블로 관리하여 감사(audit) 기능 추가 가능

---

## 문서 버전
- v1.0 (2025-12-07): 초기 설계 문서 작성

