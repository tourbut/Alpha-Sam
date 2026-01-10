import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.src.engine.price_service import price_service
from app.src.core.cache import cache_service

async def verify():
    print("🧪 Verifying PriceService Redis Integration...")
    
    # 1. Manually set a price in Redis
    test_symbol = "VERIFY_TEST"
    test_price = 1234.56
    cache_key = f"price:{test_symbol}"
    
    await cache_service.set(cache_key, str(test_price), ttl=60)
    print(f"✅ Set {cache_key} to {test_price}")
    
    # 2. Get price via PriceService
    fetched_price = await price_service.get_current_price(test_symbol)
    print(f"🔍 PriceService returned: {fetched_price}")
    
    if fetched_price == test_price:
        print("🎉 SUCCESS: PriceService correctly fetched data from Redis!")
    else:
        print("❌ FAILURE: PriceService did not return the expected price.")

    # 3. Test Mock Fallback
    mock_symbol = "BTC"
    await cache_service.delete(f"price:{mock_symbol}")
    fetched_mock = await price_service.get_current_price(mock_symbol)
    print(f"🔍 Mock Test (BTC): {fetched_mock} (Should be 100000.0 or similar)")

if __name__ == "__main__":
    asyncio.run(verify())
