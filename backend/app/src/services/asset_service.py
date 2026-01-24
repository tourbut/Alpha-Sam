import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.src.crud import assets as crud_asset
from app.src.schemas.asset import AssetCreate, AssetRead
from app.src.services.portfolio_calculator import calculate_position_metrics 
from app.src.services.price_service import price_service 
from app.src.services.portfolio_service import PortfolioService

class AssetService:
    async def get_assets_with_metrics(
        self, session: AsyncSession, user_id: uuid.UUID, portfolio_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 100
    ) -> List[AssetRead]:
        """
        자산 목록 조회 및 메트릭(평가액, 손익 등) 계산
        Position은 Transaction을 집계하여 동적으로 계산됨
        """
        # 1. Asset 목록 조회 (latest_price 포함)
        assets_data = await crud_asset.get_assets(
            session=session, owner_id=user_id, portfolio_id=portfolio_id, skip=skip, limit=limit
        )
        
        # 2. 관련 포트폴리오 식별
        # 조회된 자산들이 속한 포트폴리오 ID들을 수집
        relevant_portfolio_ids = set()
        for asset, _, _ in assets_data:
            if asset.portfolio_id:
                relevant_portfolio_ids.add(asset.portfolio_id)
        
        # 3. 각 포트폴리오별로 Position 계산
        position_map = {}  # asset_id -> PositionWithAsset
        
        for pid in relevant_portfolio_ids:
            # PortfolioService를 통해 해당 포트폴리오의 최신 포지션(가격 포함) 계산
            pf_positions = await PortfolioService.get_positions(session, pid)
            for pos in pf_positions:
                position_map[pos.asset_id] = pos
        
        # 4. AssetRead 생성 (Position 정보와 결합)
        asset_reads = []
        for asset, latest_price, latest_timestamp in assets_data:
            asset_read = AssetRead.model_validate(asset)
            
            # Latest Price 설정
            if latest_price is not None:
                asset_read.latest_price = float(latest_price) if hasattr(latest_price, '__float__') else latest_price
                asset_read.latest_price_updated_at = latest_timestamp
            
            # Position 매핑 확인
            position_obj = position_map.get(asset.id)
            
            if position_obj:
                # PortfolioService.get_positions에서 이미 valuation, profit_loss 등이 계산되어 있을 수 있음
                # 하지만, current_price가 없는 경우 등을 대비해 여기서 재확인 가능
                # get_positions는 내부적으로 calculate_position_metrics를 호출함.
                
                if position_obj.valuation is not None:
                    asset_read.valuation = position_obj.valuation
                    asset_read.profit_loss = position_obj.profit_loss
                    asset_read.return_rate = position_obj.return_rate
                else:
                    # Fallback metric calculation if not present
                    metrics = calculate_position_metrics(
                        quantity=position_obj.quantity,
                        buy_price=position_obj.avg_price,
                        current_price=float(latest_price) if latest_price is not None else None
                    )
                    asset_read.valuation = metrics["valuation"]
                    asset_read.profit_loss = metrics["profit_loss"]
                    asset_read.return_rate = metrics["return_rate"]
                
                # Position 정보도 응답에 포함
                asset_read.quantity = position_obj.quantity
                asset_read.avg_price = position_obj.avg_price
            else:
                asset_read.valuation = None
                asset_read.profit_loss = None
                asset_read.return_rate = None
                
            asset_reads.append(asset_read)
            
        return asset_reads

    async def create_asset_with_autofill(
        self, session: AsyncSession, asset_in: AssetCreate, user_id: uuid.UUID
    ) -> AssetRead:
        """
        자산 생성 (심볼 자동 검색 및 채우기 포함)
        """
        # 중복 체크 (포트폴리오 별로 유니크해야 함)
        existing_asset = await crud_asset.get_asset_by_symbol(
            session=session, 
            symbol=asset_in.symbol, 
            owner_id=user_id,
            portfolio_id=asset_in.portfolio_id
        )
        if existing_asset and (existing_asset.owner_id is None or existing_asset.owner_id == user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with symbol {asset_in.symbol} already exists in this portfolio"
            )
        
        # Auto-fill name/category if missing
        if not asset_in.name:
            results = await price_service.search_symbol(asset_in.symbol)
            match = next((r for r in results if r["symbol"] == asset_in.symbol.upper()), None)
            if not match and results:
                match = results[0]
                
            if match:
                asset_in.name = match["name"]
                if not asset_in.category and match.get("type"):
                    asset_in.category = match["type"]
            else:
                pass

        # Double check: Name is mandatory
        if not asset_in.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Asset name is required (could not auto-fill from symbol)"
            )

        # 소유자 설정
        asset_in.owner_id = user_id if asset_in.owner_id is None else asset_in.owner_id

        return await crud_asset.create_asset(session=session, obj_in=asset_in)

asset_service = AssetService()
