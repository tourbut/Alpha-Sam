from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.src.crud import crud_asset
from app.src.schemas.asset import AssetCreate, AssetRead
from app.src.engine.portfolio_service import calculate_position_metrics
from app.src.engine.price_service import price_service

class AssetService:
    async def get_assets_with_metrics(
        self, 
        session: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AssetRead]:
        """
        자산 목록 조회 및 메트릭(평가액, 손익 등) 계산
        """
        assets_data = await crud_asset.get_assets(session=session, owner_id=user_id, skip=skip, limit=limit)
        
        asset_reads = []
        for asset, latest_price, latest_timestamp, position_obj in assets_data:
            asset_read = AssetRead.model_validate(asset)
            
            if latest_price is not None:
                asset_read.latest_price = latest_price
                asset_read.latest_price_updated_at = latest_timestamp
            
            # Position이 있으면 계산된 메트릭 포함
            if position_obj:
                metrics = calculate_position_metrics(
                    quantity=position_obj.quantity,
                    buy_price=position_obj.buy_price,
                    current_price=latest_price
                )
                asset_read.valuation = metrics["valuation"]
                asset_read.profit_loss = metrics["profit_loss"]
                asset_read.return_rate = metrics["return_rate"]
                
                # Position 정보도 응답에 포함
                asset_read.quantity = position_obj.quantity
                asset_read.buy_price = position_obj.buy_price
            else:
                asset_read.valuation = None
                asset_read.profit_loss = None
                asset_read.return_rate = None
                
            asset_reads.append(asset_read)
            
        return asset_reads

    async def create_asset_with_autofill(
        self, 
        session: AsyncSession, 
        asset_in: AssetCreate, 
        user_id: int
    ) -> AssetRead:
        """
        자산 생성 (심볼 자동 검색 및 채우기 포함)
        """
        # 중복 체크
        existing_asset = await crud_asset.get_asset_by_symbol(session=session, symbol=asset_in.symbol, owner_id=user_id)
        if existing_asset and (existing_asset.owner_id is None or existing_asset.owner_id == user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with symbol {asset_in.symbol} already exists"
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
                # If auto-fill failed and name is not provided, we can't proceed
                # Instead of raising immediately here if match failed, we double check below
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
