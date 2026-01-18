import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_slash_consistency():
    """
    Test routing consistency for Trailing Slashes.
    We decided to use `""` as path for resource roots (e.g., `/api/v1/transactions`).
    This means `/api/v1/transactions` should be reachable.
    FaastAPI Default: `/api/v1/transactions/` (with slash) might redirect to without slash.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        
        # Test 1: Transactions Root
        # Without slash
        resp = await client.get("/api/v1/transactions")
        # Should be 401 (Unauthorized) or 200 (if we had auth), but definitely NOT 404 (Not Found)
        assert resp.status_code != 404, "/api/v1/transactions should operate (auth error is fine)"
        
        # With slash
        resp_slash = await client.get("/api/v1/transactions/")
        # FastAPI default behavior is usually 307 Redirect to non-slash if 'redirect_slashes' is True
        # Or 200/401 if it handles validly.
        # We just want to ensure it's not a hard 404.
        # If it is 307, follow redirect.
        if resp_slash.status_code == 307:
            loc = resp_slash.headers["location"]
            assert loc.rstrip("/") == "http://test/api/v1/transactions"
        else:
            assert resp_slash.status_code != 404, "/api/v1/transactions/ should be handled (307 or 200/401)"

        # Test 2: Assets Root
        resp = await client.get("/api/v1/assets")
        assert resp.status_code != 404
        
        resp_slash = await client.get("/api/v1/assets/")
        if resp_slash.status_code == 307:
             pass 
        else:
             assert resp_slash.status_code != 404

        # Test 3: Portfolios Root
        resp = await client.get("/api/v1/portfolios")
        assert resp.status_code != 404

        resp_slash = await client.get("/api/v1/portfolios/")
        if resp_slash.status_code == 307:
            pass
        else:
             assert resp_slash.status_code != 404
