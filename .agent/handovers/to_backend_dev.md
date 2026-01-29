# Handovers: To Backend Dev

## 날짜
- 2026-01-29

## 브랜치 (Version Control)
- `feature/backend-realized-profit`

## 현재 상황 (Context)
- 포트폴리오 조회 시 현재 보유 자산에 대한 평가 손익(`valuation`, `profit_loss`)은 계산되고 있으나, 매도(SELL)를 통해 이미 확정된 **실현 손익(Realized Profit/Loss)**이 포함되지 않고 있습니다.
- `PortfolioSummary`에 이를 포함하여 사용자가 전체 투자 성과를 볼 수 있게 해야 합니다.

## 해야 할 일 (Tasks)
1. **Schema 수정**:
   - `backend/app/src/schemas/portfolio.py`의 `PortfolioSummary` 모델에 optional 필드 `realized_pl` (float)을 추가하세요.

2. **계산 로직 개선 (`portfolio_calculator.py`)**:
   - `calculate_positions` 함수를 수정하여 `(positions, total_realized_pl)` 튜플을 반환하도록 변경하세요.
   - 내부 루프에서 `SELL` 트랜잭션 처리 시 실현 손익을 계산하여 누적하세요.
     - 공식: `realized_gain = (sell_price - avg_buy_price) * sell_quantity`
     - 주의: `avg_price`는 매도 **이전** 시점의 평단가여야 합니다.

3. **Service 연동 (`portfolio_service.py`)**:
   - `PortfolioService.get_positions` 메서드는 현재 `List[PositionWithAsset]`만 반환하므로, 내부적으로 `calculate_positions`의 반환값을 언패킹하여 `realized_pl`은 무시하거나(하위 호환), 필요한 경우 메서드 시그니처를 변경하세요.
   - **권장**: `get_positions`는 그대로 두고, `get_summary` 메서드 내에서 `realized_pl`을 활용하도록 로직을 수정하세요.
   - `PortfolioService.get_summary`에서 `PortfolioSummary` 객체 생성 시 `realized_pl` 필드를 채워 반환하세요.
   - (선택) `create_snapshot`에서도 이 값을 `PortfolioHistory.total_pl`에 반영할지 고려해보세요 (현재는 평가 손익만 저장 중일 수 있음).

## 기대 산출물 (Expected Outputs)
- `GET /api/v1/portfolios/{id}/summary` 등의 응답에 `realized_pl` 데이터가 포함됨.
- 매도 내역이 있는 포트폴리오의 경우 정확한 실현 손익이 계산됨.

## 참고 자료 (References)
- `backend/app/src/services/portfolio_calculator.py`: 핵심 비즈니스 로직
