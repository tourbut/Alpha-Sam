import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import uuid
from app.src.services.system_portfolio_service import SystemPortfolioService
from app.src.models.user import User
from app.src.models.portfolio import Portfolio
from app.src.models.asset import Asset
from app.src.models.admin import AdminAsset

class TestSystemPortfolioService(unittest.IsolatedAsyncioTestCase):
    async def test_get_or_create_system_user_success(self):
        # Mock Session
        mock_session = AsyncMock()
        
        # Mock Result
        mock_user = User(id=1, email="admin@example.com", is_superuser=True)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute.return_value = mock_result
        
        user = await SystemPortfolioService.get_or_create_system_user(mock_session)
        
        self.assertEqual(user, mock_user)
        
    async def test_get_or_create_system_user_fail(self):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        with self.assertRaises(Exception):
            await SystemPortfolioService.get_or_create_system_user(mock_session)

    @patch("app.src.services.system_portfolio_service.SystemPortfolioService.get_or_create_system_user")
    async def test_sync_admin_asset_creation(self, mock_get_user):
        # Mock User
        mock_user = User(id=1, email="admin@example.com", is_superuser=True)
        mock_get_user.return_value = mock_user
        
        # Mock Session
        mock_session = AsyncMock()
        
        # Mock Portfolio Result (Return None first time to trigger creation)
        mock_port_result = MagicMock()
        mock_port_result.scalar_one_or_none.return_value = None
        
        # Mock Asset Result (Return None to trigger creation)
        mock_asset_result = MagicMock()
        mock_asset_result.scalar_one_or_none.return_value = None
        
        # Configure execute side effects
        # 1. get_portfolio -> None
        # 2. get_existing_asset -> None
        mock_session.execute.side_effect = [mock_port_result, mock_asset_result]
        
        # Input Admin Asset
        admin_asset = AdminAsset(
            id=uuid.uuid4(),
            symbol="KRW=X",
            name="USD/KRW",
            type="EXCHANGE_RATE",
            is_active=True
        )
        
        # Call
        asset = await SystemPortfolioService.sync_admin_asset_to_system(mock_session, admin_asset)
        
        # Assertions
        self.assertIsNotNone(asset)
        self.assertEqual(asset.symbol, "KRW=X")
        self.assertEqual(asset.category, "EXCHANGE_RATE")
        
        # Verify add was called for Portfolio and Asset
        self.assertEqual(mock_session.add.call_count, 2) 

    @patch("app.src.services.system_portfolio_service.SystemPortfolioService.get_or_create_system_user")
    async def test_sync_admin_asset_skip_type(self, mock_get_user):
        mock_session = AsyncMock()
        
        # Input Admin Asset (STOCK type)
        admin_asset = AdminAsset(
            id=uuid.uuid4(),
            symbol="AAPL",
            name="Apple",
            type="STOCK",
            is_active=True
        )
        
        asset = await SystemPortfolioService.sync_admin_asset_to_system(mock_session, admin_asset)
        
        self.assertIsNone(asset)
