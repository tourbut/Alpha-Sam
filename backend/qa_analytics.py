import json
import urllib.request
import urllib.error
import urllib.parse
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "analytics_test@example.com"
PASSWORD = "password123"
NICKNAME = "AnalyticsTester"

def request(method, endpoint, data=None, headers=None):
    if headers is None:
        headers = {}
    url = BASE_URL + endpoint
    if data:
        json_data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    else:
        json_data = None
    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode('utf-8')
            try: return status, json.loads(body)
            except: return status, body
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8')
        try: return status, json.loads(body)
        except: return status, body
    except Exception as e:
        return 0, str(e)

def run_verification():
    print(f"Checking backend analytics at {BASE_URL}...")
    try:
        # 1. Login/Signup
        print("1. Authenticating...")
        data = urllib.parse.urlencode({"username": EMAIL, "password": PASSWORD}).encode('utf-8')
        req = urllib.request.Request(BASE_URL + "/auth/login", data=data, method="POST")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        token = None
        try:
            with urllib.request.urlopen(req) as r:
                token = json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError:
             print("   Login failed, trying signup...")
             status, resp = request("POST", "/auth/signup", data={"email": EMAIL, "password": PASSWORD, "nickname": NICKNAME})
             if status in [201, 400]:
                 try:
                    with urllib.request.urlopen(req) as r:
                        token = json.loads(r.read().decode('utf-8'))
                 except: pass

        if not token:
            print("   Failed to authenticate.")
            sys.exit(1)
            
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        print("   Authentication successful.")
        
        # 2. Setup Data
        print("2. Setting up test data (Portfolio, Asset, TX)...")
        status, resp = request("POST", "/portfolios", data={"name": "Analytics Test Portfolio", "currency": "USD"}, headers=headers)
        if status != 201:
             print(f"   Failed to create portfolio: {resp}")
             sys.exit(1)
        portfolio_id = resp['id']
        
        status, resp = request("POST", "/assets", data={"portfolio_id": portfolio_id, "symbol": "AAPL", "name": "Apple", "category": "STOCK"}, headers=headers)
        if status != 201:
             print(f"   Failed to create asset AAPL: {resp}")
             sys.exit(1)
        asset_aapl = resp['id']
        
        request("POST", f"/portfolios/{portfolio_id}/transactions", data={"portfolio_id": portfolio_id, "asset_id": asset_aapl, "type": "BUY", "quantity": 10.0, "price": 100.0, "executed_at": "2026-02-01T12:00:00"}, headers=headers)
        print("   Setup complete.")
        
        # 3. Test Analytics
        print("3. Testing Analytics Allocation...")
        status, resp = request("GET", f"/analytics/portfolio/{portfolio_id}/allocation", headers=headers)
        print(f"   Status: {status}")
        if status != 200:
            print(f"   Failed Allocation: {resp}")
            sys.exit(1)
        print(f"   Allocation Data: {resp}")
        
        print("4. Testing Analytics History...")
        status, resp = request("GET", f"/analytics/portfolio/{portfolio_id}/history?range=1M", headers=headers)
        print(f"   Status: {status}")
        if status != 200:
            print(f"   Failed History: {resp}")
            sys.exit(1)
        print(f"   History length: {len(resp)} entries")
        
        # Cleanup
        print("5. Cleanup...")
        request("DELETE", f"/portfolios/{portfolio_id}", headers=headers)
        print("   Cleanup done.")
        
        print("\nSUCCESS: Analytics endpoints passed!")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
