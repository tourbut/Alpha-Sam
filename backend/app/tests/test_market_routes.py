import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

class TestMarketRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_search_symbol_route(self):
        with patch("app.src.routes.market.price_service") as mock_price_service:
            # Setup mock return value
            mock_price_service.search_symbol = AsyncMock(return_value=[
                {"symbol": "AAPL", "name": "Apple Inc.", "type": "EQUITY", "exchange": "NMS"}
            ])
            
            response = self.client.get("/api/v1/market/search?q=Apple")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["symbol"], "AAPL")

    def test_validate_symbol_route(self):
        with patch("app.src.routes.market.price_service") as mock_price_service:
            # Setup mock return value
            mock_price_service.validate_symbol = AsyncMock(return_value=True)
            
            response = self.client.get("/api/v1/market/validate?symbol=AAPL")
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["symbol"], "AAPL")
            self.assertTrue(data["valid"])
