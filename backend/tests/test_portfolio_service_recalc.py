import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from app.src.engine.portfolio_service import PortfolioService

# Mock Transaction
class MockTransaction:
    def __init__(self, id, type, quantity, price, executed_at):
        self.id = id
        self.type = type
        self.quantity = float(quantity)
        self.price = float(price)
        self.executed_at = executed_at

@pytest.mark.asyncio
async def test_recalculate_position_logic():
    service = PortfolioService()
    session = AsyncMock()
    
    # Mock query result for transactions
    # Scenario:
    # 1. Buy 10 @ 100
    # 2. Buy 10 @ 200 -> Avg 150
    # 3. Sell 5 @ 300 -> Avg 150, Qty 15
    # 4. Buy 5 @ 100 -> Qty 20, Cost (15*150 + 5*100) = 2250 + 500 = 2750. Avg = 2750/20 = 137.5
    
    transactions = [
        MockTransaction(1, "BUY", 10, 100, "2026-01-01"),
        MockTransaction(2, "BUY", 10, 200, "2026-01-02"),
        MockTransaction(3, "SELL", 5, 300, "2026-01-03"),
        MockTransaction(4, "BUY", 5, 100, "2026-01-04"),
    ]
    
    # Mock session.execute to return the transactions
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = transactions
    session.execute.return_value = mock_result
    
    # Mock existing position check (return None to create new)
    mock_pos_result = MagicMock()
    mock_pos_result.scalar_one_or_none.return_value = None
    
    # We need to handle multiple calls to execute (transactions query, then position query)
    # Side effect for session.execute
    async def execute_side_effect(stmt):
        # We can't easily check stmt content in simple mock, so we assume order
        # But wait, recalculate calls execute twice.
        # 1. Select Transactions
        # 2. Select Position
        return mock_result if "FROM transactions" in str(stmt) else mock_pos_result

    # Let's simplify: 
    # The logic is inside _recalculate_position. We can test the logic by extracting it or 
    # trusting the mocks. 
    # Ideally we'd test the `calculate` logic heavily.
    
    # For this test, let's create a separate testable function or verify the mock calls.
    # Since we can't easily run the actual DB query, we will rely on injecting the mocks.
    
    # But wait, the service fetches transactions inside the method.
    # We can mock session.execute to return different results based on call count if logic is strictly sequential.
    session.execute = AsyncMock(side_effect=[mock_result, mock_pos_result])
    
    # Run
    await service._recalculate_position(session, portfolio_id=1, asset_id=1)
    
    # Verify session.add was called with correct Position
    # Expected:
    # Qty: 15 (Buy 20, Sell 5) + 5 = 20
    # Avg: 137.5 (as calculated above)
    
    args, _ = session.add.call_args
    position = args[0]
    
    assert position.quantity == 20.0
    assert position.avg_price == 137.5
    assert position.portfolio_id == 1
    assert position.asset_id == 1

@pytest.mark.asyncio
async def test_recalculate_position_sell_all():
    service = PortfolioService()
    session = AsyncMock()
    
    transactions = [
        MockTransaction(1, "BUY", 10, 100, "2026-01-01"),
        MockTransaction(2, "SELL", 10, 120, "2026-01-02"),
    ]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = transactions
    mock_pos_result = MagicMock()
    mock_pos_result.scalar_one_or_none.return_value = None
    
    session.execute = AsyncMock(side_effect=[mock_result, mock_pos_result])
    
    await service._recalculate_position(session, portfolio_id=1, asset_id=1)
    
    args, _ = session.add.call_args
    position = args[0]
    
    assert position.quantity == 0.0
    assert position.avg_price == 0.0

