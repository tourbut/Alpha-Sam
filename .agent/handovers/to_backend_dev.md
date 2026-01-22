# Handovers: To Backend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/backend-portfolio-summary` (from `develop`)

## 현재 상황 (Context)
- 1. 자산 조회(`get_asset_by_symbol`) 시 동일 심볼이 여러 포트폴리오에 존재할 수 있어 `portfolio_id` 구분이 필요함.
- 2. 포트폴리오 요약 조회(`get_summary`) 시 `portfolio_id` 없이 호출하면 첫 번째 포트폴리오만 반환하고 있음(전체 합산 필요).

## 해야 할 일 (Tasks)
1. `app/src/services/portfolio_service.py`의 `get_summary` 메서드 수정:
   - `portfolio_id`가 `None`인 경우, 사용자의 **모든 포트폴리오**를 조회.
   - 각 포트폴리오의 포지션을 모두 합산하여 전체 자산 현황과 요약(Total Value, PL 등)을 반환하도록 로직 변경.
2. `app/src/routes/assets.py` (또는 해당 기능 라우터) 수정:
   - `get_asset_by_symbol` (또는 자산 조회) 엔드포인트에 `portfolio_id` 파라미터(Optional) 추가.
   - 서비스/CRUD 호출 시 `portfolio_id`를 전달하여 정확한 자산을 찾도록 수정.

## 기대 산출물 (Expected Outputs)
- 대시보드 등에서 전체 요약 조회 시 모든 포트폴리오의 합산 데이터가 반환됨.
- 자산 추가/조회 시 포트폴리오별로 정확한 자산이 식별됨.
