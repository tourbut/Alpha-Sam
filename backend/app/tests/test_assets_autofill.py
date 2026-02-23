import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.src.schemas.asset import AssetCreate

class TestAssetAutoFill(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        from app.src.deps import get_current_user
        from app.src.models.user import User
        
        async def mock_get_current_user():
            return User(id=1, email="test@example.com", is_active=True)
            
        app.dependency_overrides[get_current_user] = mock_get_current_user

    def tearDown(self):
        from app.src.deps import get_current_user
        app.dependency_overrides.pop(get_current_user, None)

    @patch("app.src.services.asset_service.crud_asset")
    @patch("app.src.services.asset_service.price_service")
    def test_create_asset_autofill_success(self, mock_price_service, mock_crud_asset):
        # Mock dependencies
        mock_crud_asset.get_asset_by_symbol = AsyncMock(return_value=None)
        mock_crud_asset.create_asset = AsyncMock(return_value={
            "id": "e45e23c0-1fb4-4bcf-bbb8-84f38cd0d2fb", "symbol": "AAPL", "name": "Apple Inc.", "category": "EQUITY", 
            "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00",
            "portfolio_id": "e45e23c0-1fb4-4bcf-bbb8-84f38cd0d2fb"
        })
        
        mock_price_service.search_symbol = AsyncMock(return_value=[
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "EQUITY"}
        ])
        
        import uuid
        dummy_portfolio_id = str(uuid.uuid4())
        # Test request with missing name
        response = self.client.post("/api/v1/assets/", json={"symbol": "AAPL", "portfolio_id": dummy_portfolio_id})
        
        self.assertEqual(response.status_code, 201)
        
        # Verify crud_asset.create_asset was called with populated name
        args, kwargs = mock_crud_asset.create_asset.call_args
        obj_in = kwargs["obj_in"]
        self.assertEqual(obj_in.name, "Apple Inc.")
        self.assertEqual(obj_in.category, "EQUITY")

    @patch("app.src.services.asset_service.crud_asset")
    @patch("app.src.services.asset_service.price_service")
    def test_create_asset_autofill_fail(self, mock_price_service, mock_crud_asset):
        # Mock dependencies
        mock_crud_asset.get_asset_by_symbol = AsyncMock(return_value=None)
        
        # Mock search returns empty
        mock_price_service.search_symbol = AsyncMock(return_value=[])
        
        import uuid
        dummy_portfolio_id = str(uuid.uuid4())
        # Test request with missing name
        response = self.client.post("/api/v1/assets/", json={"symbol": "UNKNOWN", "portfolio_id": dummy_portfolio_id})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Asset name is required", response.json()["detail"])
