from typing import List, Dict, Optional, Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.schemas.position import PositionWithAsset
from app.src.schemas.portfolio import PortfolioResponse, PortfolioSummary, PortfolioStats, PortfolioSharedRead
from app.src.services.portfolio_calculator import calculate_position_metrics, calculate_portfolio_summary, calculate_positions
from app.src.crud import portfolios as crud_portfolio
from app.src.crud import assets as crud_asset
from app.src.crud import transactions as crud_transaction
from sqlalchemy.orm import selectinload

class PortfolioService:
    @staticmethod
    async def _get_portfolio_core_data(session: AsyncSession, portfolio_id: uuid.UUID) -> tuple[List[PositionWithAsset], float]:
        """
        Internal helper to fetch data, calculate positions and realized P/L, and enrich with prices.
        Returns (positions, realized_pl)
        """
        # 1. Fetch Assets
        from app.src.models.asset import Asset
        stmt_asset = select(Asset).where(Asset.portfolio_id == portfolio_id)
        result_asset = await session.execute(stmt_asset)
        assets = result_asset.scalars().all()
        
        if not assets:
            return [], 0.0

        # 2. Fetch Transactions
        from app.src.models.transaction import Transaction
        stmt_tx = (
            select(Transaction)
            .where(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.executed_at, Transaction.id)
        )
        result_tx = await session.execute(stmt_tx)
        transactions = result_tx.scalars().all()
        
        # 3. Call Engine
        # Returns (positions, realized_pl)
        positions, realized_pl = calculate_positions(assets=assets, transactions=transactions)
        
        # 4. Enhance with Prices
        if positions:
            from app.src.services.price_service import price_service
            
            for position in positions:
                symbol = position.asset_symbol
                current_price = 0.0
                if symbol:
                    current_price = await price_service.get_current_price(symbol)
                
                # Re-calculate metrics with price
                metrics = calculate_position_metrics(
                    quantity=position.quantity,
                    buy_price=position.avg_price,
                    current_price=current_price
                )
                
                position.valuation = metrics["valuation"]
                position.profit_loss = metrics["profit_loss"]
                position.return_rate = metrics["return_rate"]
                position.current_price = current_price

        return positions, realized_pl

    @staticmethod
    async def get_positions(session: AsyncSession, portfolio_id: uuid.UUID) -> List[PositionWithAsset]:
        positions, _ = await PortfolioService._get_portfolio_core_data(session, portfolio_id)
        return positions

    @staticmethod
    async def update_visibility(session: AsyncSession, portfolio_id: uuid.UUID, visibility: PortfolioVisibility) -> Optional[Portfolio]:
        return await crud_portfolio.update_visibility(session=session, portfolio_id=portfolio_id, visibility=visibility)

    @staticmethod
    async def get_shared_portfolio(session: AsyncSession, token: uuid.UUID) -> Optional[PortfolioSharedRead]:
        portfolio = await crud_portfolio.get_shared_portfolio(session=session, token=token)
        
        if not portfolio:
            return None
        
        if portfolio.visibility == PortfolioVisibility.PRIVATE:
            return None

        # 1. Calculate Positions
        positions, realized_pl = await PortfolioService._get_portfolio_core_data(session, portfolio.id)
        
        total_value = 0.0
        portfolio_return_rate = 0.0
        
        summary_input_data = []

        if positions:
             for position in positions:
                summary_input_data.append({
                    "quantity": float(position.quantity),
                    "buy_price": float(position.avg_price),
                    "current_price": position.current_price
                })
            
             summary_metrics = calculate_portfolio_summary(summary_input_data)
             total_value = summary_metrics["total_valuation"] or 0.0
             portfolio_return_rate = summary_metrics["portfolio_return_rate"] or 0.0

        # Owner nickname
        from app.src.models.user import User
        user = await session.get(User, portfolio.owner_id)
        owner_nickname = user.nickname if user else "Unknown"

        return PortfolioSharedRead(
            id=portfolio.id,
            name=portfolio.name,
            owner_nickname=owner_nickname,
            description=portfolio.description,
            total_value=total_value,
            return_rate=portfolio_return_rate,
            positions=positions,
            visibility=portfolio.visibility
        )
        portfolios = []
        if portfolio_id:
            portfolio = await crud_portfolio.get_portfolio(session=session, portfolio_id=portfolio_id)
            if portfolio:
                portfolios.append(portfolio)
        else:
            portfolios = await crud_portfolio.get_user_portfolios(session=session, owner_id=user_id)
        
        if not portfolios:
            return PortfolioResponse(
                summary=PortfolioSummary(
                    total_value=0.0,
                    total_cost=0.0,
                    total_pl=0.0,
                    total_pl_stats=PortfolioStats(percent=0.0, direction="flat")
                ),
                positions=[]
            )
        
        all_positions_map: Dict[uuid.UUID, PositionWithAsset] = {}
        total_realized_pl_all = 0.0
        
        for portfolio in portfolios:
            positions, realized_pl = await PortfolioService._get_portfolio_core_data(session, portfolio.id)
            total_realized_pl_all += realized_pl
            
            for pos in positions:
                if pos.asset_id in all_positions_map:
                    existing = all_positions_map[pos.asset_id]
                    
                    total_qty = existing.quantity + pos.quantity
                    cost1 = existing.quantity * existing.avg_price
                    cost2 = pos.quantity * pos.avg_price
                    total_cost = cost1 + cost2
                    new_avg_price = (total_cost / total_qty) if total_qty > 0 else 0.0
                    
                    existing.quantity = total_qty
                    existing.avg_price = new_avg_price
                    # Prices should be same for same asset
                else:
                    all_positions_map[pos.asset_id] = pos

        final_positions = list(all_positions_map.values())
        
        # Prices are already enriched in get_positions, so we just calculate summary
        summary_input_data = []
        for position in final_positions:
             summary_input_data.append({
                "quantity": float(position.quantity),
                "buy_price": float(position.avg_price),
                "current_price": position.current_price
            })

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
            realized_pl=total_realized_pl_all,
            total_pl_stats=PortfolioStats(
                percent=summary_metrics["portfolio_return_rate"],
                direction=direction
            )
        )

        return PortfolioResponse(
            summary=summary_schema,
            positions=final_positions
        )



    @staticmethod
    async def get_portfolios_with_assets(session: AsyncSession, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        from app.src.schemas.portfolio import PortfolioAssetSummary, PortfolioWithAssetsSummary
        
        portfolios = await crud_portfolio.get_user_portfolios(session=session, owner_id=user_id)
        
        if not portfolios:
            return []
        
        portfolio_responses = []
        
        for portfolio in portfolios:
            positions, _ = await PortfolioService._get_portfolio_core_data(session, portfolio.id)
            
            total_value = 0.0
            asset_summaries = []
            
            # Positions already have prices from get_positions
            
            position_values = []
            for position in positions:
                # Use pre-calculated valuation if available (since get_positions does it)
                valuation = position.valuation if position.valuation is not None else (position.quantity * position.avg_price)
                 
                position_values.append({
                    "symbol": position.asset_symbol or "UNKNOWN",
                    "name": position.asset_name or "Unknown Asset",
                    "value": round(valuation, 2),
                    "asset_id": position.asset_id
                })
                total_value += valuation
            
            if total_value > 0:
                for pv in position_values:
                    percentage = (pv["value"] / total_value) * 100
                    asset_summaries.append(PortfolioAssetSummary(
                        symbol=pv["symbol"],
                        name=pv["name"],
                        value=pv["value"],
                        percentage=round(percentage, 1)
                    ))
            
            portfolio_with_assets = PortfolioWithAssetsSummary(
                id=portfolio.id,
                name=portfolio.name,
                currency=portfolio.currency,
                description=portfolio.description,
                created_at=portfolio.created_at,
                total_value=round(total_value, 2),
                assets=asset_summaries
            )
            portfolio_responses.append(portfolio_with_assets)
        
        return portfolio_responses
