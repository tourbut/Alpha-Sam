import urllib.request
import urllib.parse
import json
import secrets
import ssl
import time

# Bypass SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = f"qa_analytics_{secrets.token_hex(4)}@test.com"
PASSWORD = "password123"

def make_request(url, method="GET", data=None, headers={}):
    try:
        req = urllib.request.Request(url, method=method)
        for k, v in headers.items():
            req.add_header(k, v)
        
        if data:
            json_data = json.dumps(data).encode("utf-8")
            req.add_header("Content-Type", "application/json")
            req.data = json_data
            
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)

def login(email, password):
    url = f"{BASE_URL}/auth/login"
    data = urllib.parse.urlencode({"username": email, "password": password}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")

print(f"--- QA Analytics Script: {EMAIL} ---")

# 1. Signup
print("1. Signup")
status, body = make_request(f"{BASE_URL}/auth/signup", method="POST", data={"email": EMAIL, "password": PASSWORD, "nickname": "Analyst"})
if status != 201:
    print(f"Signup Failed: {status} {body}")
    # Try Login
else:
    print("Signup OK")

# 2. Login
print("2. Login")
status, body = login(EMAIL, PASSWORD)
if status != 200:
    print(f"Login Failed: {status} {body}")
    exit(1)
token = json.loads(body)["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("Login OK")

# 3. Create Asset (BTC-USD)
print("3. Create Asset (BTC-USD)")
asset_id = None
asset_data = {"name": "Bitcoin", "symbol": "BTC-USD", "asset_type": "Crypto", "sector": "Digital"}
status, body = make_request(f"{BASE_URL}/assets/", method="POST", data=asset_data, headers=headers)
if status == 201:
    asset_id = json.loads(body)["id"]
    print(f"Created Asset ID: {asset_id}")
elif status == 400: # Already exists
    print("Asset exists, finding ID...")
    status, body = make_request(f"{BASE_URL}/assets/", method="GET", headers=headers)
    if status == 200:
        assets = json.loads(body)
        target = next((a for a in assets if a["symbol"] == "BTC-USD"), None)
        if target:
            asset_id = target["id"]
            print(f"Found Asset ID: {asset_id}")
            # Ensure price update?
            make_request(f"{BASE_URL}/prices/refresh", method="POST", headers=headers) 

if not asset_id:
    print("Failed to get Asset ID")
    exit(1)

# 4. Create Position
print("4. Create Position")
# Buy 0.5 BTC at $20000
position_data = {"asset_id": asset_id, "quantity": 0.5, "buy_price": 20000.0}
status, body = make_request(f"{BASE_URL}/positions/", method="POST", data=position_data, headers=headers)
if status != 201:
    print(f"Create Position Failed: {status} {body}")
    exit(1)
print("Position Created")

# Wait for price fetch?
print("Waiting 2s for price...")
time.sleep(2)

# 5. Get Portfolio Summary
print("5. Get Portfolio Summary")
status, body = make_request(f"{BASE_URL}/portfolio/summary", method="GET", headers=headers)
if status != 200:
    print(f"Get Portfolio Failed: {status} {body}")
else:
    data = json.loads(body)
    summary = data["summary"]
    print("--- Summary ---")
    print(json.dumps(summary, indent=2))
    
    positions = data["positions"]
    print(f"Positions Count: {len(positions)}")
    if len(positions) > 0:
        pos = positions[0]
        print(f"Pos 1: {pos['asset_symbol']} Qty: {pos['quantity']} Val: {pos['valuation']} PL: {pos['profit_loss']}")
        
    if summary["total_value"] and summary["total_value"] > 0:
        print("✅ Analytics Verification SUCCESS")
    else:
        print("❌ Analytics Verification FAILED (Zero Value - Price might be missing)")

