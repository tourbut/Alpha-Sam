from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.src.models.position import Position
from app.src.models.price import Price
from app.src.models.portfolio_history import PortfolioHistory
from app.src.schemas.position import PositionWithAsset
from app.src.schemas.portfolio import PortfolioResponse, PortfolioSummary, PortfolioStats
from app.src.engine.portfolio_service import calculate_position_metrics, calculate_portfolio_summary
from app.src.crud import crud_portfolio_history
from sqlalchemy.orm import selectinload

class PortfolioService:
    @staticmethod
    async def create_snapshot(session: AsyncSession, user_id: int) -> PortfolioHistory:
        """
        Create a portfolio snapshot for the given user.
        """
        # 1. Fetch all positions
        stmt = select(Position).where(Position.owner_id == user_id)
        result = await session.execute(stmt)
        positions = result.scalars().all()
        
        summary_input_data = []

        if positions:
            # 2. Fetch latest prices (Batch)
            asset_ids = [p.asset_id for p in positions]
            price_map = await PortfolioService._get_latest_prices(session, asset_ids)
        else:
            price_map = {}

        for position in positions:
            current_price = price_map.get(position.asset_id)
            summary_input_data.append({
                "quantity": float(position.quantity),
                "buy_price": float(position.buy_price),
                "current_price": current_price
            })

        # 3. Calculate Summary
        summary_metrics = calculate_portfolio_summary(summary_input_data)
        
        # 4. Save History
        history = PortfolioHistory(
            owner_id=user_id,
            total_value=summary_metrics["total_valuation"] or 0.0,
            total_cost=summary_metrics["total_invested"] or 0.0,
            total_pl=summary_metrics["total_profit_loss"] or 0.0
        )
        
        await crud_portfolio_history.create_portfolio_history(session=session, history=history)
        return history

    @staticmethod
    async def get_summary(session: AsyncSession, user_id: int) -> PortfolioResponse:
        """
        Get portfolio summary and positions.
        """
        # 1. Fetch positions with Asset
        stmt = (
            select(Position)
            .where(Position.owner_id == user_id)
            .options(selectinload(Position.asset))
        )
        result = await session.execute(stmt)
        positions = result.scalars().all()
        
        if not positions:
            return PortfolioResponse(
                summary=PortfolioSummary(
                    total_value=0.0,
                    total_cost=0.0,
                    total_pl=0.0,
                    total_pl_stats=PortfolioStats(percent=0.0, direction="flat")
                ),
                positions=[]
            )

        # 2. Fetch Prices
        asset_ids = [p.asset_id for p in positions]
        price_map = await PortfolioService._get_latest_prices(session, asset_ids)
        
        position_reads: List[PositionWithAsset] = []
        summary_input_data = []

        for position in positions:
            asset = position.asset
            current_price = price_map.get(position.asset_id)
            
            metrics = calculate_position_metrics(
                quantity=position.quantity,
                buy_price=position.buy_price,
                current_price=current_price
            )
            
            position_dict = {
                "id": position.id,
                "asset_id": position.asset_id,
                "quantity": float(position.quantity),
                "buy_price": float(position.buy_price),
                "buy_date": position.buy_date,
                "created_at": position.created_at,
                "updated_at": position.updated_at,
                "valuation": metrics["valuation"],
                "profit_loss": metrics["profit_loss"],
                "return_rate": metrics["return_rate"],
                "current_price": current_price,
                "asset_symbol": asset.symbol if asset else None,
                "asset_name": asset.name if asset else None,
                "asset_category": asset.category if asset else None,
            }
            position_reads.append(PositionWithAsset(**position_dict))
            
            summary_input_data.append({
                "quantity": float(position.quantity),
                "buy_price": float(position.buy_price),
                "current_price": current_price
            })

        # 3. Calculate Summary
        summary_metrics = calculate_portfolio_summary(summary_input_data)
        total_pl = summary_metrics["total_profit_loss"]
        
        direction = "flat"
        if total_pl is not None:
            if total_pl > 0:
                direction = "up"
            elif total_pl < 0:
                direction = "down"

        summary_schema = PortfolioSummary(
            total_value=summary_metrics["total_valuation"],
            total_cost=summary_metrics["total_invested"],
            total_pl=summary_metrics["total_profit_loss"],
            total_pl_stats=PortfolioStats(
                percent=summary_metrics["portfolio_return_rate"],
                direction=direction
            )
        )

        return PortfolioResponse(
            summary=summary_schema,
            positions=position_reads
        )

    @staticmethod
    async def _get_latest_prices(session: AsyncSession, asset_ids: List[int]) -> Dict[int, float]:
        """
        Helper to fetch latest prices for given assets efficiently.
        """
        if not asset_ids:
            return {}
            
        stmt = (
            select(Price)
            .distinct(Price.asset_id)
            .where(Price.asset_id.in_(asset_ids))
            .order_by(Price.asset_id, desc(Price.timestamp))
        )
        result = await session.execute(stmt)
        latest_prices = result.scalars().all()
        
        return {price.asset_id: price.value for price in latest_prices}
