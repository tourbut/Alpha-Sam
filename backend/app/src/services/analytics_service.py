from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
import uuid
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from app.src.models.portfolio import Portfolio
from app.src.models.transaction import Transaction
from app.src.models.asset import Asset
from app.src.schemas.analytics import AssetAllocationResponse, PortfolioHistoryResponse
from app.src.services.portfolio_calculator import calculate_positions

async def get_portfolio_allocation(
    session: AsyncSession,
    portfolio_id: uuid.UUID
) -> List[AssetAllocationResponse]:
    """
    Get asset allocation (pie chart data) for a portfolio.
    Calculates current positions and their valuations.
    """
    # 1. Fetch all assets and transactions for the portfolio
    query_assets = select(Asset).join(Transaction).where(Transaction.portfolio_id == portfolio_id).distinct()
    result_assets = await session.execute(query_assets)
    assets = result_assets.scalars().all()
    
    query_tx = select(Transaction).where(Transaction.portfolio_id == portfolio_id).order_by(Transaction.executed_at.asc())
    result_tx = await session.execute(query_tx)
    transactions = result_tx.scalars().all()
    
    if not assets or not transactions:
        return []
        
    # 2. Calculate current positions
    positions, _ = calculate_positions(list(assets), list(transactions))
    
    # 3. Fetch current prices (Mocking for now as per v2.0 current logic or simple base)
    # Ideally prices are updated here. For allocation, we need valuation.
    total_portfolio_value = 0.0
    allocations = []
    
    # Simulating a basic valuation calculation if current_price is 0/None.
    # In a real scenario, use price_service to get latest prices.
    for pos in positions:
        # Fallback to avg_price if current_price is missing to show SOME allocation
        price_to_use = pos.current_price if pos.current_price is not None and pos.current_price > 0 else pos.avg_price
        valuation = pos.quantity * price_to_use
        if valuation > 0:
            total_portfolio_value += valuation
            allocations.append({
                "ticker": pos.asset_symbol,
                "value": valuation
            })
            
    # Calculate percentages
    response = []
    for alloc in allocations:
        percentage = (alloc["value"] / total_portfolio_value * 100) if total_portfolio_value > 0 else 0.0
        response.append(
            AssetAllocationResponse(
                ticker=alloc["ticker"],
                percentage=round(percentage, 2),
                total_value=round(alloc["value"], 2)
            )
        )
        
    # Sort by percentage descending
    response.sort(key=lambda x: x.percentage, reverse=True)
    return response

async def get_portfolio_history(
    session: AsyncSession,
    portfolio_id: uuid.UUID,
    range: str = "1M"
) -> List[PortfolioHistoryResponse]:
    """
    Get portfolio value history (line chart data).
    On-the-fly calculation by replaying transactions day by day.
    """
    # 1. Determine date range
    end_date = date.today()
    start_date = end_date
    
    if range == "1W":
        start_date = end_date - timedelta(days=7)
    elif range == "1M":
        start_date = end_date - relativedelta(months=1)
    elif range == "1Y":
        start_date = end_date - relativedelta(years=1)
    elif range == "YTD":
        start_date = date(end_date.year, 1, 1)
    else: # ALL
        start_date = date(2000, 1, 1) # Will be clamped to first tx later
        
    # 2. Fetch transactions up to end_date
    query_tx = select(Transaction).where(
        Transaction.portfolio_id == portfolio_id,
        func.date(Transaction.executed_at) <= end_date
    ).order_by(Transaction.executed_at.asc())
    
    result_tx = await session.execute(query_tx)
    transactions = result_tx.scalars().all()
    
    if not transactions:
        return []
        
    # Clamp start_date to first transaction date if 'ALL' or before first tx
    first_tx_date = transactions[0].executed_at.date()
    if start_date < first_tx_date:
        start_date = first_tx_date
        
    # 3. Simulate day-by-day accumulation
    history = []
    current_date = start_date
    tx_idx = 0
    num_tx = len(transactions)
    
    # State tracking
    cumulative_invested = 0.0
    holdings = {} # asset_id -> {qty, cost}
    
    # Fast-forward state to start_date
    while tx_idx < num_tx and transactions[tx_idx].executed_at.date() < start_date:
        tx = transactions[tx_idx]
        qty = float(tx.quantity)
        price = float(tx.price)
        value = qty * price
        
        if tx.asset_id not in holdings:
            holdings[tx.asset_id] = {"qty": 0.0, "cost": 0.0}
            
        if tx.type == "BUY":
            holdings[tx.asset_id]["qty"] += qty
            cumulative_invested += value
        elif tx.type == "SELL":
            holdings[tx.asset_id]["qty"] = max(0.0, holdings[tx.asset_id]["qty"] - qty)
            cumulative_invested -= value # Rough uninvested cash approximation for now
            
        tx_idx += 1

    # Daily simulation
    while current_date <= end_date:
        # Process transactions for current_date
        while tx_idx < num_tx and transactions[tx_idx].executed_at.date() == current_date:
            tx = transactions[tx_idx]
            qty = float(tx.quantity)
            price = float(tx.price)
            value = qty * price
            
            if tx.asset_id not in holdings:
                holdings[tx.asset_id] = {"qty": 0.0}
                
            if tx.type == "BUY":
                holdings[tx.asset_id]["qty"] += qty
                cumulative_invested += value
            elif tx.type == "SELL":
                holdings[tx.asset_id]["qty"] = max(0.0, holdings[tx.asset_id]["qty"] - qty)
                cumulative_invested -= value
                
            tx_idx += 1
            
        # Calculate EOD Value (Using Last Traded Price as mock for EOD price)
        # Real app needs historical daily price series per asset.
        daily_value = 0.0
        for asset_id, data in holdings.items():
            # Mock EOD price calculation - assuming avg price is current price for rough chart
            # We will just accumulate invested amount as a placeholder if no prices
            asset_qty = data["qty"]
            # Just rough fallback to invested.
            pass
            
        # For simplicity in this v2.1.0 on-the-fly approach without historical price DB, 
        # we will plot cumulative_invested as total_value if prices are missing, 
        # but realistically we just sum up holding quantities * latest prices.
        # Here we mock it as cumulative_invested * some noise for demonstration, or just flat invested.
        mock_eod_value = cumulative_invested # Replace with actual query to historical prices
        
        history.append(
            PortfolioHistoryResponse(
                date=current_date.strftime("%Y-%m-%d"),
                total_value=round(max(0, mock_eod_value), 2),
                uninvested_cash=0.0 # To be implemented fully when cash model is added
            )
        )
        current_date += timedelta(days=1)
        
    return history
