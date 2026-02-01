import json
import uuid
import sys
import urllib.request
import urllib.error
import urllib.parse
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "update_test@example.com"
PASSWORD = "password123"
NICKNAME = "UpdateTester"

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
            try:
                json_body = json.loads(body)
            except:
                json_body = body
            return status, json_body
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8')
        try:
             json_body = json.loads(body)
        except:
             json_body = body
        return status, json_body
    except Exception as e:
        print(f"Request Error: {e}")
        return 0, str(e)

def run_verification():
    print(f"Checking backend at {BASE_URL}...")
    try:
        # 1. Authenticate (Login or Signup)
        print("1. Authenticating...")
        # Try Login (Form Data)
        data = urllib.parse.urlencode({"username": EMAIL, "password": PASSWORD}).encode('utf-8')
        req = urllib.request.Request(BASE_URL + "/auth/login", data=data, method="POST")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        token = None
        try:
            with urllib.request.urlopen(req) as r:
                resp = json.loads(r.read().decode('utf-8'))
                token = resp
        except urllib.error.HTTPError as e:
             # If login fails, try signup
             print("   Login failed, trying signup...")
             status, resp = request("POST", "/auth/signup", data={"email": EMAIL, "password": PASSWORD, "nickname": NICKNAME})
             if status in [201, 400]:
                 # Try login again
                 try:
                    with urllib.request.urlopen(req) as r:
                        resp = json.loads(r.read().decode('utf-8'))
                        token = resp
                 except:
                     pass

        if not token:
            print("   Failed to authenticate.")
            sys.exit(1)
            
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        print("   Authentication successful.")
        
        # 2. Create Portfolio
        print("2. Creating Portfolio...")
        status, resp = request("POST", "/portfolios", data={"name": "Update Test Portfolio", "currency": "USD"}, headers=headers)
        if status != 201:
             print(f"   Failed to create portfolio: {resp}")
             sys.exit(1)
        portfolio_id = resp['id']
        print(f"   Portfolio created ({portfolio_id}).")

        # 3. Create Asset
        print("3. Creating Asset...")
        status, resp = request("POST", "/assets", data={
            "portfolio_id": portfolio_id,
            "symbol": "UPDT", 
            "name": "Update Token", 
            "category": "CRYPTO"
        }, headers=headers)
        if status != 201:
             print(f"   Failed to create asset: {resp}")
             sys.exit(1)
        asset_id = resp['id']
        print(f"   Asset created ({asset_id}).")
        
        # 4. Update Asset
        print("4. Updating Asset...")
        new_name = "Updated Token Name"
        status, resp = request("PUT", f"/assets/{asset_id}", data={"name": new_name}, headers=headers)
        if status != 200:
            print(f"   Failed to update asset: {resp}")
            sys.exit(1)
        if resp['name'] != new_name:
            print(f"   Asset update mismatch: {resp['name']}")
            sys.exit(1)
        print("   Asset update verified.")

        # 5. Create Transaction
        print("5. Creating Transaction...")
        status, resp = request("POST", f"/portfolios/{portfolio_id}/transactions", data={
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "type": "BUY",
            "quantity": 10.0,
            "price": 100.0,
            "executed_at": "2026-02-01T12:00:00"
        }, headers=headers)
        if status != 201:
            print(f"   Failed to create transaction: {resp}")
            sys.exit(1)
        transaction_id = resp['id']
        print(f"   Transaction created ({transaction_id}).")
        
        # 6. Update Transaction
        print("6. Updating Transaction...")
        new_quantity = 20.0
        # Determine URL based on typical route registration
        # Assuming /transactions/{id} or /api/v1/transactions/{id}
        # Based on routes/transactions.py appearing to be top-level or under /transactions
        status, resp = request("PUT", f"/transactions/{transaction_id}", data={"quantity": new_quantity}, headers=headers)
        
        if status == 404:
             # Try /portfolios/... path if not found (though code put it in routes/transactions.py)
             print("   /transactions/{id} not found, trying /portfolios/... (unlikely based on code)")
        
        if status != 200:
            print(f"   Failed to update transaction: {resp} (Status: {status})")
            sys.exit(1)
            
        if float(resp['quantity']) != new_quantity:
            print(f"   Transaction update mismatch: {resp['quantity']}")
            sys.exit(1)
        print("   Transaction update verified.")
        
        # Cleanup
        print("7. Cleanup...")
        request("DELETE", f"/portfolios/{portfolio_id}", headers=headers)
        print("   Cleanup done.")
        
        print("\nSUCCESS: Update functionality verified!")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
