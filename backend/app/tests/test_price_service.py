import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from app.src.engine.price_service import PriceService

class TestPriceService(unittest.IsolatedAsyncioTestCase):
    async def test_search_symbol_success(self):
        service = PriceService()
        
        mock_response_data = {
            "quotes": [
                {
                    "symbol": "AAPL",
                    "shortname": "Apple Inc.",
                    "quoteType": "EQUITY",
                    "exchange": "NMS"
                }
            ]
        }
        
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_resp.__aenter__.return_value = mock_resp
            mock_resp.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value = mock_resp
            
            results = await service.search_symbol("Apple")
            
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["symbol"], "AAPL")
            self.assertEqual(results[0]["name"], "Apple Inc.")

    async def test_search_symbol_empty(self):
        service = PriceService()
        
        mock_response_data = {"quotes": []}
        
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_resp.__aenter__.return_value = mock_resp
            mock_resp.json = AsyncMock(return_value=mock_response_data)
            mock_get.return_value = mock_resp
            
            results = await service.search_symbol("InvalidQuery")
            
            self.assertEqual(len(results), 0)

    async def test_validate_symbol_valid(self):
        service = PriceService()
        
        # Mock get_current_price to return a valid price (async)
        with patch.object(service, "get_current_price", new_callable=AsyncMock) as mock_price:
            mock_price.return_value = 150.0
            is_valid = await service.validate_symbol("AAPL")
            self.assertTrue(is_valid)

    async def test_validate_symbol_invalid(self):
        service = PriceService()
        
        # Mock get_current_price to return 0 (async)
        with patch.object(service, "get_current_price", new_callable=AsyncMock) as mock_price:
            mock_price.return_value = 0.0
            is_valid = await service.validate_symbol("INVALID")
            self.assertFalse(is_valid)
