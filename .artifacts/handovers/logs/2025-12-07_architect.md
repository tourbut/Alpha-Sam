# Handovers: To Architect

## 날짜
2025-12-07

## 현재 상황 (Context)
- Alpha-Sam 프로젝트의 기본 구조는 완성되었습니다 (Asset, Price 모델 및 API 구현 완료).
- 하지만 도메인 규칙에 명시된 **Position/Holding 모델**이 아직 구현되지 않았습니다.
- 현재 프론트엔드에서 수익률/평가액을 표시하려고 하지만, 백엔드에서 Position 정보와 계산 로직이 없어 데이터가 표시되지 않습니다.

## 해야 할 일 (Tasks)
1. Position/Holding 모델의 데이터베이스 스키마를 설계합니다.
   - `domain_rules.md`의 Position 규칙을 참고하여 다음 필드를 포함:
     - `id`: 고유 ID
     - `asset_id`: Asset 참조 (Foreign Key)
     - `quantity`: 보유 수량 (0 이상)
     - `buy_price`: 매수 단가 (0 초과)
     - `buy_date`: 매수 일자 (선택적)
     - `created_at`, `updated_at`: 타임스탬프
2. Asset과 Position의 관계를 명확히 정의합니다.
   - 한 Asset에 여러 Position이 있을 수 있는지, 아니면 1:1 관계인지 결정.
   - (일반적으로는 한 Asset당 하나의 Position만 허용하는 것이 일반적)
3. 수익률 계산 로직의 위치를 결정합니다.
   - 백엔드 API에서 계산하여 반환할지, 프론트엔드에서 계산할지 결정.
   - (권장: 백엔드에서 계산하여 일관성 유지)
4. Alembic 마이그레이션 파일 작성을 위한 스키마 변경사항을 문서화합니다.

## 기대 산출물 (Expected Outputs)
- Position 모델의 스키마 설계 문서 (또는 코드 주석으로 명시)
- Asset-Position 관계 정의 문서
- 수익률 계산 로직 위치 결정 및 설계 문서
- 다음 단계(백엔드 개발자에게 전달할)를 위한 명확한 설계 가이드

## 참고 자료 (References)
- `.artifacts/prompts/projects/alphha_sam/domain_rules.md` (Position 필드 규칙, 수익률 계산 규칙)
- `.artifacts/prompts/projects/alphha_sam/context.md` (프로젝트 목표 및 주요 기능)
- `backend/app/models/asset.py` (기존 Asset 모델 참고)
- `backend/app/models/price.py` (기존 Price 모델 참고)

---

## 작업 완료 내역

### 완료된 작업
✅ Position/Holding 모델의 데이터베이스 스키마 설계 완료
✅ Asset-Position 관계 정의 완료 (1:1 관계로 결정)
✅ 수익률 계산 로직 위치 결정 완료 (백엔드에서 계산)
✅ Alembic 마이그레이션 가이드 문서화 완료

### 산출물
- **설계 문서**: `.artifacts/prompts/projects/alphha_sam/position_model_design.md`
  - Position 모델 스키마 상세 설계
  - Asset-Position 1:1 관계 정의 및 근거
  - 수익률 계산 로직 위치 및 구현 가이드
  - Alembic 마이그레이션 가이드
  - 백엔드 개발자를 위한 구현 순서 및 참고사항

### 주요 설계 결정
1. **관계 유형**: Asset : Position = 1:1 (UNIQUE 제약으로 보장)
2. **수익률 계산**: 백엔드 API에서 수행 (일관성, 정합성, 보안)
3. **계산 로직 위치**: 서비스 레이어 (`portfolio_service.py`)
4. **에지 케이스**: 시세 없음, 0으로 나누기 등 명시적 처리

### 다음 단계
백엔드 개발자가 `.artifacts/prompts/projects/alphha_sam/position_model_design.md` 문서를 참고하여 Position 모델 및 API를 구현할 수 있습니다.
