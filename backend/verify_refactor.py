import json
import uuid
import sys
import urllib.request
import urllib.error
import urllib.parse

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "refactor_test@example.com"
PASSWORD = "password123"
NICKNAME = "RefactorTester"

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
        # 1. Signup/Login
        print("1. Authenticating...")
        # Try login
        status, resp = request("POST", "/auth/login", data={"username": EMAIL, "password": PASSWORD}) # Auth form is form-data usually?
        
        # Wait! OAuth2PasswordRequestForm expects FORM DATA, not JSON.
        # Urllib needs form encoding for this.
        if status != 200:
             # Try Signup (JSON)
             print("   Login failed, trying signup...")
             status, resp = request("POST", "/auth/signup", data={"email": EMAIL, "password": PASSWORD, "nickname": NICKNAME})
             if status in [201, 400]:
                 # Login again
                 # Authenticate with FORM DATA
                 data = urllib.parse.urlencode({"username": EMAIL, "password": PASSWORD}).encode('utf-8')
                 req = urllib.request.Request(BASE_URL + "/auth/login", data=data, method="POST")
                 req.add_header('Content-Type', 'application/x-www-form-urlencoded')
                 try:
                     with urllib.request.urlopen(req) as r:
                         status = r.status
                         resp = json.loads(r.read().decode('utf-8'))
                 except urllib.error.HTTPError as e:
                     status = e.code
                     resp = json.loads(e.read().decode('utf-8'))

        if status != 200:
            # Maybe first login attempt failed because I sent JSON instead of Form?
            # Let's retry login with Form Data if first failed.
            data = urllib.parse.urlencode({"username": EMAIL, "password": PASSWORD}).encode('utf-8')
            req = urllib.request.Request(BASE_URL + "/auth/login", data=data, method="POST")
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            try:
                with urllib.request.urlopen(req) as r:
                    status = r.status
                    resp = json.loads(r.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                status = e.code
                resp = json.loads(e.read().decode('utf-8'))
        
        if status != 200:
            print(f"   Failed to login: {resp}")
            sys.exit(1)
            
        token = resp
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        print("   Authentication successful.")
        
        # 2. Create Portfolio
        print("2. Creating Portfolio...")
        status, resp = request("POST", "/portfolios", data={"name": "Refactor Portfolio", "description": "Testing CRUD refactor", "currency": "USD"}, headers=headers)
        if status != 201:
            print(f"   Failed to create portfolio: {resp}")
            sys.exit(1)
        portfolio_id = resp['id']
        print(f"   Portfolio created ({portfolio_id}).")

        # 3. Create Asset
        print("3. Ensuring Asset 'REFx'...")
        asset_id = None
        status, assets = request("GET", f"/assets?portfolio_id={portfolio_id}", headers=headers)
        if status == 200:
            for a in assets:
                if a['symbol'] == "REFx" and a.get('portfolio_id') == portfolio_id:
                    asset_id = a['id']
                    break
        
        if not asset_id:
            status, resp = request("POST", "/assets", data__={
                "portfolio_id": portfolio_id,
                "symbol": "REFx", 
                "name": "Refactor Token", 
                "category": "CRYPTO"
            }, headers=headers) # Typo data__ -> data
            # Fix typo in my variable above: data__
            
            status, resp = request("POST", "/assets", data={
                "portfolio_id": portfolio_id,
                "symbol": "REFx", 
                "name": "Refactor Token", 
                "category": "CRYPTO"
            }, headers=headers)

            if status == 201:
                asset_id = resp['id']
                print("   Asset created.")
            else:
                print(f"   Failed to create asset: {resp}")
                # Try delete portfolio
                request("DELETE", f"/portfolios/{portfolio_id}", headers=headers)
                sys.exit(1)
        else:
            print(f"   Asset 'REFx' found ({asset_id}).")
            
        # 4. Create Transaction
        print("4. Creating Transaction (Route Refactor Verify)...")
        tx_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "type": "BUY",
            "quantity": 10.5,
            "price": 100.0,
            "executed_at": "2026-01-31T12:00:00"
        }
        status, resp = request("POST", f"/portfolios/{portfolio_id}/transactions", data=tx_data, headers=headers)
        if status != 201:
             print(f"   Failed to create transaction: {resp}")
             sys.exit(1)
        print("   Transaction created.")
        
        # 5. Read Asset Transactions
        print("5. Reading Asset Transactions (Route Refactor Verify)...")
        status, txs = request("GET", f"/portfolios/{portfolio_id}/assets/{asset_id}/transactions", headers=headers)
        if status != 200:
            print(f"   Failed to get transactions: {txs}")
            sys.exit(1)
            
        if len(txs) > 0:
            print(f"   Transactions retrieved: {len(txs)} items.")
        else:
            print("   Error: No transactions returned.")
            sys.exit(1)
            
        # 6. Delete Portfolio
        print("6. Deleting Portfolio (CRUD Refactor Verify)...")
        status, resp = request("DELETE", f"/portfolios/{portfolio_id}", headers=headers)
        if status != 204:
            print(f"   Failed to delete portfolio: {resp}")
            sys.exit(1)
        print("   Portfolio deleted.")
        
        # 7. Verify Deletion
        status, resp = request("GET", f"/portfolios/{portfolio_id}", headers=headers)
        if status == 404:
            print("   Verification successful: Portfolio not found.")
        else:
            print(f"   Error: Portfolio still exists? Status: {status}")
            sys.exit(1)
            
        print("\nSUCCESS: All refactor verification steps passed!")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
