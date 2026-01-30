# Handovers: To Architect

## 날짜
- 2026-01-30

## 브랜치 (Version Control)
- `feature/system-portfolio-strategy`

## 현재 상황 (Context)
- 사용자로부터 `USD/KRW` 등 환율 정보를 시스템에서 관리하고 `PriceDay` 테이블을 활용해 시세를 수집/제공해달라는 요청이 있었습니다.
- 현재 `PriceDay`는 `Asset`(`portfolio_id` 필수)에 종속되어 있어, 전역적인(Global) 자산 관리를 위한 전략이 필요합니다.

## 해야 할 일 (Tasks)
1. **System Portfolio 설계**:
   - 시스템 관리용 유저(`system_admin`)와 시스템 포트폴리오(`System Portfolio`)를 정의하고, 이를 통해 전역 자산(환율, 지수 등)을 관리하는 방안을 수립하세요.
   - `AdminAsset` (메타데이터 정의)과 `Asset` (시스템 포트폴리오 내 인스턴스) 간의 동기화 규칙을 정의하세요.

2. **데이터 모델링 가이드**:
   - `AssetType`에 `EXCHANGE_RATE`를 추가하고, 환율 심볼 포맷(예: Yahoo Finance `KRW=X`)에 대한 표준을 정의하세요.

## 기대 산출물 (Expected Outputs)
- `.agent/project/system_architecture.md` (또는 유사 문서)에 System Portfolio 및 Global Asset 관리 전략 문서화.

## 참고 자료 (References)
- `backend/app/src/models/asset.py`
- `backend/app/src/services/tasks/price_tasks.py`
