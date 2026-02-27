import httpx
import asyncio
import json

API_URL = "http://127.0.0.1:8000"

async def main():
    async with httpx.AsyncClient(base_url=API_URL) as client:
        print("=== 1. Agent Login ===")
        login_data = {"username": "tester@example.com", "password": "password123"}
        resp = await client.post("/api/v1/agent/login", data=login_data)
        
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return
            
        data = resp.json()
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("V Login Success! Token acquired.")
        
        print("\n=== 2. Create Portfolio ===")
        pf_data = {"name": "Agent Test Portfolio", "description": "Automated E2E Test", "currency": "USD"}
        resp = await client.post("/api/v1/portfolios", json=pf_data, headers=headers)
        resp.raise_for_status()
        portfolio = resp.json()
        pf_id = portfolio["id"]
        print(f"V Created Portfolio: {portfolio['name']} (ID: {pf_id})")
        
        print("\n=== 3. Add Asset ===")
        asset_data = {
            "portfolio_id": pf_id,
            "symbol": "NVDA", 
            "name": "NVIDIA", 
            "category": "Stock"
        }
        resp = await client.post("/api/v1/assets", json=asset_data, headers=headers)
        resp.raise_for_status()
        asset = resp.json()
        asset_id = asset["id"]
        print(f"V Added Asset: {asset['symbol']} (ID: {asset_id})")
        
        print("\n=== 4. Record Transaction ===")
        tx_data = {
            "portfolio_id": pf_id,
            "asset_id": asset_id,
            "type": "BUY",
            "quantity": 5.0,
            "price": 120.0,
            "executed_at": "2026-02-24T12:00:00Z"
        }
        resp = await client.post("/api/v1/transactions", json=tx_data, headers=headers)
        resp.raise_for_status()
        tx = resp.json()
        print(f"V Recorded BUY Transaction: {tx['quantity']} NVDA @ ${tx['price']}")
        
        print("\n=== 5. Fetch Portfolio List ===")
        resp = await client.get("/api/v1/portfolios", headers=headers)
        resp.raise_for_status()
        portfolios = resp.json()
        print(f"V Found {len(portfolios)} total portfolios. First one: {portfolios[0]['name']}")
        
        print("\n=== 6. Fetch Current Positions ===")
        resp = await client.get(f"/api/v1/portfolios/{pf_id}/positions", headers=headers)
        resp.raise_for_status()
        positions = resp.json()
        print(f"V Current Positions summary:")
        print(json.dumps(positions, indent=2))
        
        print("\n=== E2E Test Completed Successfully ===")

if __name__ == "__main__":
    asyncio.run(main())
