# Handovers: To Backend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `fix/backend-position-calc` (from `develop`)

## 현재 상황 (Context)
- 포트폴리오에 자산(`Asset`)을 추가했지만 트랜잭션(`Transaction`)이 없으면 자산 목록(Position)에 표시되지 않는 문제.
- `calculate_positions_from_transactions` 함수가 트랜잭션이 있는 경우만 계산하여 반환하고 있음.

## 해야 할 일 (Tasks)
1. `backend/app/src/engine/portfolio_service.py`의 `calculate_positions_from_transactions` 함수 수정.
   - 1단계: 해당 `portfolio_id`를 가진 모든 `Asset`을 조회.
   - 2단계: `Transaction`을 조회하여 자산별로 매핑.
   - 3단계: 트랜잭션이 없는 자산도 포함하여 `PositionWithAsset` 객체 생성 (quantity=0, avg_price=0 등 초기값).
   - 4단계: `if current_qty > 0` 조건 제거 (모든 자산 반환).

## 기대 산출물 (Expected Outputs)
- 포트폴리오 상세 조회 시, 트랜잭션이 없는 초기 자산도 목록에 표시됨(수량 0).
