import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.src.schemas.asset import AssetCreate

class TestAssetAutoFill(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.src.routes.assets.crud_asset")
    @patch("app.src.routes.assets.price_service")
    def test_create_asset_autofill_success(self, mock_price_service, mock_crud_asset):
        # Mock dependencies
        mock_crud_asset.get_asset_by_symbol = AsyncMock(return_value=None)
        mock_crud_asset.create_asset = AsyncMock(return_value={
            "id": 1, "symbol": "AAPL", "name": "Apple Inc.", "category": "EQUITY", 
            "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00"
        })
        
        mock_price_service.search_symbol = AsyncMock(return_value=[
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "EQUITY"}
        ])
        
        # Test request with missing name
        response = self.client.post("/api/v1/assets/", json={"symbol": "AAPL"})
        
        self.assertEqual(response.status_code, 201)
        
        # Verify crud_asset.create_asset was called with populated name
        args, kwargs = mock_crud_asset.create_asset.call_args
        obj_in = kwargs["obj_in"]
        self.assertEqual(obj_in.name, "Apple Inc.")
        self.assertEqual(obj_in.category, "EQUITY")

    @patch("app.src.routes.assets.crud_asset")
    @patch("app.src.routes.assets.price_service")
    def test_create_asset_autofill_fail(self, mock_price_service, mock_crud_asset):
        # Mock dependencies
        mock_crud_asset.get_asset_by_symbol = AsyncMock(return_value=None)
        
        # Mock search returns empty
        mock_price_service.search_symbol = AsyncMock(return_value=[])
        
        # Test request with missing name
        response = self.client.post("/api/v1/assets/", json={"symbol": "UNKNOWN"})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name is required", response.json()["detail"])
