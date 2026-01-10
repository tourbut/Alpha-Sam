import unittest
from unittest.mock import AsyncMock, patch
from app.src.engine.asset_service import AssetService

class TestAssetListing(unittest.IsolatedAsyncioTestCase):
    @patch("app.src.engine.asset_service.crud_asset")
    async def test_get_assets_with_metrics_call_signature(self, mock_crud_asset):
        """
        Verify that AssetService.get_assets_with_metrics calls crud_asset.get_assets
        using ONLY keyword arguments, as crud_asset.get_assets enforces `*` (keyword-only).
        """
        # Setup
        mock_crud_asset.get_assets = AsyncMock(return_value=[])
        service = AssetService()
        mock_session = AsyncMock()
        
        # Action
        await service.get_assets_with_metrics(session=mock_session, user_id=1, skip=0, limit=10)
        
        # Verification
        # Check call arguments of the mock
        args, kwargs = mock_crud_asset.get_assets.call_args
        
        # The critical check: args should be empty. 
        # If session was passed positionally, len(args) would be > 0.
        self.assertEqual(len(args), 0, "All arguments to crud_asset.get_assets must be keyword arguments")
        
        # Verify correct values passed in kwargs
        self.assertIn("session", kwargs)
        self.assertEqual(kwargs["session"], mock_session)
        self.assertIn("owner_id", kwargs)
        self.assertEqual(kwargs["owner_id"], 1)
