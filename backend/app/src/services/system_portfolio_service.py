from typing import Optional
import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.models.user import User
from app.src.models.portfolio import Portfolio, PortfolioVisibility
from app.src.models.asset import Asset
from app.src.models.admin import AdminAsset

logger = logging.getLogger(__name__)

class SystemPortfolioService:
    SYSTEM_PORTFOLIO_NAME = "System Portfolio"
    
    @staticmethod
    async def get_or_create_system_user(session: AsyncSession) -> User:
        """
        시스템 관리용 유저(Superuser)를 조회.
        DB에 존재하는 슈퍼유저 중 첫 번째를 사용.
        """
        stmt = select(User).where(User.is_superuser == True).limit(1)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            logger.error("No superuser found in DB. Cannot manage System Portfolio.")
            raise Exception("System requires at least one superuser.")
            
        return user

    @staticmethod
    async def get_or_create_system_portfolio(session: AsyncSession) -> Portfolio:
        """
        시스템 포트폴리오를 조회하거나 생성.
        """
        system_user = await SystemPortfolioService.get_or_create_system_user(session)
        
        # 이름으로 조회
        stmt = select(Portfolio).where(
            Portfolio.owner_id == system_user.id,
            Portfolio.name == SystemPortfolioService.SYSTEM_PORTFOLIO_NAME
        )
        result = await session.execute(stmt)
        portfolio = result.scalar_one_or_none()
        
        if not portfolio:
            logger.info(f"Creating System Portfolio for user {system_user.email}")
            portfolio = Portfolio(
                owner_id=system_user.id,
                name=SystemPortfolioService.SYSTEM_PORTFOLIO_NAME,
                description="Managed by System for Global Assets (Exchange Rates, Indices, etc.)",
                visibility=PortfolioVisibility.PRIVATE # 시스템 내부용
            )
            session.add(portfolio)
            await session.commit()
            await session.refresh(portfolio)
            
        return portfolio

    @staticmethod
    async def sync_admin_asset_to_system(session: AsyncSession, admin_asset: AdminAsset) -> Optional[Asset]:
        """
        AdminAsset이 EXCHANGE_RATE (또는 시스템 관리가 필요한 타입)일 경우,
        System Portfolio 내에 해당 Asset을 생성/동기화한다.
        """
        # 동기화 대상 타입 정의
        TARGET_TYPES = ["EXCHANGE_RATE", "FOREX", "INDEX"]
        
        if admin_asset.type not in TARGET_TYPES and admin_asset.type != "EXCHANGE_RATE": 
            # "EXCHANGE_RATE"는 새로 추가될 타입
            # 기존 FOREX, INDEX도 시스템 자산으로 관리하고 싶다면 여기에 포함.
            # 일단 요구사항인 EXCHANGE_RATE만 처리해도 됨.
            if admin_asset.type != "EXCHANGE_RATE":
                return None

        system_portfolio = await SystemPortfolioService.get_or_create_system_portfolio(session)
        
        # 이미 존재하는지 확인
        stmt = select(Asset).where(
            Asset.portfolio_id == system_portfolio.id,
            Asset.symbol == admin_asset.symbol
        )
        result = await session.execute(stmt)
        existing_asset = result.scalar_one_or_none()
        
        if existing_asset:
            # 정보 업데이트 (필요시)
            if existing_asset.name != admin_asset.name:
                existing_asset.name = admin_asset.name
                session.add(existing_asset)
                # await session.commit() # 호출자가 commit하도록 유도할 수도 있음. 여기선 바로 반영
            return existing_asset
        
        # 생성
        new_asset = Asset(
            portfolio_id=system_portfolio.id,
            owner_id=system_portfolio.owner_id,
            symbol=admin_asset.symbol,
            name=admin_asset.name,
            category=admin_asset.type
        )
        session.add(new_asset)
        # await session.commit()
        
        return new_asset

system_portfolio_service = SystemPortfolioService()
