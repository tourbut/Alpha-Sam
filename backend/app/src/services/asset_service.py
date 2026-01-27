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
        assets = await crud_asset.get_assets(
            session=session, owner_id=user_id, portfolio_id=portfolio_id, skip=skip, limit=limit
        )

        assets_data = []
        
        for asset in assets:
            # Latest price
            current_price = await price_service.get_current_price(asset.symbol, use_cache=True)
            
            assets_data.append((asset, current_price))
        # 2. 관련 포트폴리오 식별
        # 조회된 자산들이 속한 포트폴리오 ID들을 수집
        relevant_portfolio_ids = set()
        for asset,_ in assets_data:
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
        for asset, latest_price in assets_data:
            asset_read = AssetRead.model_validate(asset)
            
            # Latest Price 설정
            if latest_price is not None:
                asset_read.latest_price = float(latest_price) if hasattr(latest_price, '__float__') else latest_price
            
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
            
            
        # 5. 전체 조회(portfolio_id is None)인 경우 Symbol 기준 Aggregation 수행
        if portfolio_id is None:
            return self._aggregate_assets_by_symbol(asset_reads)

        return asset_reads

    def _aggregate_assets_by_symbol(self, assets: List[AssetRead]) -> List[AssetRead]:
        """
        심볼을 기준으로 자산들을 병합(Aggregation)합니다.
        - 수량, 평가액, 손익: 합산
        - 평단가: 가중 평균
        - 그 외 필드(ID 등): 첫 번째 자산의 값 사용
        """
        grouped: Dict[str, List[AssetRead]] = {}
        for asset in assets:
            if asset.symbol not in grouped:
                grouped[asset.symbol] = []
            grouped[asset.symbol].append(asset)
        
        aggregated_results = []
        
        for symbol, group in grouped.items():
            if not group:
                continue
                
            # 대표 자산 (첫 번째 요소)
            representative = group[0]
            
            # 하나만 있으면 그대로 반환
            if len(group) == 1:
                aggregated_results.append(representative)
                continue
            
            # 합산 변수 초기화
            total_quantity = 0.0
            total_valuation = 0.0
            total_profit_loss = 0.0
            total_cost_basis = 0.0 # 평단가 계산용 (avg_price * quantity)
            
            # Aggregation Loop
            for item in group:
                qty = item.quantity or 0.0
                val = item.valuation or 0.0
                pl = item.profit_loss or 0.0
                avg = item.avg_price or 0.0
                
                total_quantity += qty
                total_valuation += val
                total_profit_loss += pl
                total_cost_basis += (avg * qty)
            
            # 결과 객체 생성 (대표 객체 복사)
            # Pydantic v2 copy() usage or constructing new
            aggregated = representative.model_copy()
            
            aggregated.quantity = total_quantity
            aggregated.valuation = total_valuation
            aggregated.profit_loss = total_profit_loss
            
            # 평단가 (가중 평균)
            if total_quantity > 0:
                aggregated.avg_price = total_cost_basis / total_quantity
            else:
                aggregated.avg_price = 0.0
                
            # 단순 별칭도 업데이트
            aggregated.buy_price = aggregated.avg_price
            
            # 수익률 재계산: (평가액 - 투자원금) / 투자원금 * 100
            # 투자원금 = total_cost_basis
            if total_cost_basis > 0:
                aggregated.return_rate = ((total_valuation - total_cost_basis) / total_cost_basis) * 100
            else:
                aggregated.return_rate = 0.0
            
            aggregated_results.append(aggregated)
            
        return aggregated_results

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
