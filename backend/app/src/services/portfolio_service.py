from typing import List, Dict, Optional, Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.src.models.price import Price
from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.models.portfolio_history import PortfolioHistory
from app.src.schemas.position import PositionWithAsset
from app.src.schemas.portfolio import PortfolioResponse, PortfolioSummary, PortfolioStats, PortfolioSharedRead
from app.src.engine.portfolio_service import calculate_position_metrics, calculate_portfolio_summary, calculate_positions_from_transactions
from app.src.crud import crud_portfolio_history
from sqlalchemy.orm import selectinload

class PortfolioService:
    @staticmethod
    async def update_visibility(session: AsyncSession, portfolio_id: int, visibility: PortfolioVisibility) -> Portfolio:
        """
        Update portfolio visibility and manage share_token.
        """
        stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await session.execute(stmt)
        portfolio = result.scalar_one_or_none()
        
        if not portfolio:
            return None
            
        portfolio.visibility = visibility
        
        if visibility == PortfolioVisibility.LINK_ONLY:
            if not portfolio.share_token:
                portfolio.share_token = uuid.uuid4()
        elif visibility == PortfolioVisibility.PRIVATE:
            portfolio.share_token = None
            
        session.add(portfolio)
        await session.commit()
        await session.refresh(portfolio)
        return portfolio

    @staticmethod
    async def get_shared_portfolio(session: AsyncSession, token: uuid.UUID) -> Optional[PortfolioSharedRead]:
        """
        Get portfolio by share_token for public/link usage.
        """
        stmt = select(Portfolio).where(Portfolio.share_token == token)
        result = await session.execute(stmt)
        portfolio = result.scalar_one_or_none()
        
        if not portfolio:
            return None
        
        # LINK_ONLY가 아니면 token으로 접근 불가? -> 설계상 LINK_ONLY일때 토큰 사용.
        # PUBLIC이어도 토큰이 있으면 접근 허용 가능.
        # 하지만 LINK_ONLY/PUBLIC 상태가 아니면 접근 불가 처리해야 함.
        if portfolio.visibility == PortfolioVisibility.PRIVATE:
            return None

        # Calculate Summary logic reused
        # 1. Transaction 기반으로 Positions 계산
        positions = await calculate_positions_from_transactions(session, portfolio.id)
        
        total_value = 0.0
        total_cost = 0.0
        portfolio_return_rate = 0.0
        
        position_reads: List[PositionWithAsset] = []
        
        if positions:
            # 2. Fetch Prices
            asset_ids = [p.asset_id for p in positions]
            price_map = await PortfolioService._get_latest_prices(session, asset_ids)
            
            summary_input_data = []

            for position in positions:
                current_price = price_map.get(position.asset_id)
                metrics = calculate_position_metrics(
                    quantity=position.quantity,
                    buy_price=position.avg_price,
                    current_price=current_price
                )
                position.valuation = metrics["valuation"]
                position.profit_loss = metrics["profit_loss"]
                position.return_rate = metrics["return_rate"]
                position.current_price = current_price
                position_reads.append(position)
                
                summary_input_data.append({
                    "quantity": float(position.quantity),
                    "buy_price": float(position.avg_price),
                    "current_price": current_price
                })
            
            # 3. Calculate Summary
            summary_metrics = calculate_portfolio_summary(summary_input_data)
            total_value = summary_metrics["total_valuation"] or 0.0
            total_cost = summary_metrics["total_invested"] or 0.0
            
            if total_cost > 0:
                portfolio_return_rate = ((total_value - total_cost) / total_cost) * 100
            
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
            positions=position_reads,
            visibility=portfolio.visibility
        )

    @staticmethod
    async def create_snapshot(session: AsyncSession, user_id: int) -> PortfolioHistory:
        """
        Create a portfolio snapshot for the given user.
        """
        # TODO: 여러 Portfolio를 지원하려면 모든 Portfolio의 Position을 합산해야 함
        # 일단은 user의 첫 번째 Portfolio를 사용
        from app.src.models.portfolio import Portfolio
        stmt_portfolio = select(Portfolio).where(Portfolio.owner_id == user_id).limit(1)
        result_portfolio = await session.execute(stmt_portfolio)
        portfolio = result_portfolio.scalar_one_or_none()
        
        if not portfolio:
            # Portfolio가 없으면 빈 snapshot 생성
            history = PortfolioHistory(
                owner_id=user_id,
                total_value=0.0,
                total_cost=0.0,
                total_pl=0.0
            )
            await crud_portfolio_history.create_portfolio_history(session=session, history=history)
            return history
        
        # 1. Transaction 기반으로 Positions 계산
        positions = await calculate_positions_from_transactions(session, portfolio.id)
        
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
                "buy_price": float(position.avg_price),
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
        with open("/Users/shin/.gemini/antigravity/brain/fe135e23-aef4-4cc1-b5ab-914a5d85fdd6/debug_log.txt", "a") as f:
            f.write(f"[DEBUG] PortfolioService.get_summary called for user_id={user_id}\n")
        
        # TODO: 여러 Portfolio를 지원하려면 모든 Portfolio의 Position을 합산해야 함
        # 일단은 user의 첫 번째 Portfolio를 사용
        from app.src.models.portfolio import Portfolio
        stmt_portfolio = select(Portfolio).where(Portfolio.owner_id == user_id).limit(1)
        result_portfolio = await session.execute(stmt_portfolio)
        portfolio = result_portfolio.scalar_one_or_none()
        
        if not portfolio:
            return PortfolioResponse(
                summary=PortfolioSummary(
                    total_value=0.0,
                    total_cost=0.0,
                    total_pl=0.0,
                    total_pl_stats=PortfolioStats(percent=0.0, direction="flat")
                ),
                positions=[]
            )
        
        # 1. Transaction 기반으로 Positions 계산
        positions = await calculate_positions_from_transactions(session, portfolio.id)
        
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
            current_price = price_map.get(position.asset_id)
            
            metrics = calculate_position_metrics(
                quantity=position.quantity,
                buy_price=position.avg_price,
                current_price=current_price
            )
            
            # Position 데이터 업데이트 (계산된 필드 추가)
            position.valuation = metrics["valuation"]
            position.profit_loss = metrics["profit_loss"]
            position.return_rate = metrics["return_rate"]
            position.current_price = current_price
            
            position_reads.append(position)
            
            summary_input_data.append({
                "quantity": float(position.quantity),
                "buy_price": float(position.avg_price),
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
        
        return {price.asset_id: float(price.value) for price in latest_prices}
