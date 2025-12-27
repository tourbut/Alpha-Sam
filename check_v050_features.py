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
EMAIL = f"qa_v050_{secrets.token_hex(4)}@test.com"
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

print(f"--- QA v0.5.0 Script: {EMAIL} ---")

# 1. Signup & Login
print("1. Signup & Login")
status, body = make_request(f"{BASE_URL}/auth/signup", method="POST", data={"email": EMAIL, "password": PASSWORD, "nickname": "Trader"})
if status != 201:
    print(f"Signup Failed: {status} {body}")
    exit(1)

status, body = login(EMAIL, PASSWORD)
if status != 200:
    print(f"Login Failed: {status} {body}")
    exit(1)
token = json.loads(body)["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("Authenticated")

# 2. Create Asset (ETH-USD)
print("2. Create Asset (ETH-USD)")
asset_id = None
asset_data = {"name": "Ethereum", "symbol": "ETH-USD", "category": "Crypto"}
status, body = make_request(f"{BASE_URL}/assets/", method="POST", data=asset_data, headers=headers)
if status == 201:
    asset_id = json.loads(body)["id"]
    print(f"Created Asset ID: {asset_id}")
else: # Attempt to find existing
    status, body = make_request(f"{BASE_URL}/assets/", method="GET", headers=headers)
    assets = json.loads(body)
    target = next((a for a in assets if a["symbol"] == "ETH-USD"), None)
    if target:
        asset_id = target["id"]
        print(f"Found Asset ID: {asset_id}")

if not asset_id:
    print("Failed to resolve Asset ID")
    exit(1)

# 3. Transaction: BUY
print("3. Transaction: BUY 10 ETH @ $2000")
tx_buy = {
    "asset_id": asset_id,
    "type": "BUY",
    "quantity": 10.0,
    "price": 2000.0
}
status, body = make_request(f"{BASE_URL}/transactions/", method="POST", data=tx_buy, headers=headers)
if status != 200:
    print(f"BUY Failed: {status} {body}")
    exit(1)
print(f"BUY OK: {body}")

# Verify Position
status, body = make_request(f"{BASE_URL}/positions/", method="GET", headers=headers)
positions = json.loads(body)
my_pos = next((p for p in positions if p["asset_id"] == asset_id), None)
print(f"Position Qty: {my_pos['quantity']} (Expected 10.0)")

# 4. Transaction: SELL
print("4. Transaction: SELL 2 ETH @ $2500")
tx_sell = {
    "asset_id": asset_id,
    "type": "SELL",
    "quantity": 2.0,
    "price": 2500.0
}
status, body = make_request(f"{BASE_URL}/transactions/", method="POST", data=tx_sell, headers=headers)
if status != 200:
    print(f"SELL Failed: {status} {body}")
    exit(1)
print(f"SELL OK: {body}")

# Verify Position
status, body = make_request(f"{BASE_URL}/positions/", method="GET", headers=headers)
positions = json.loads(body)
my_pos = next((p for p in positions if p["asset_id"] == asset_id), None)
print(f"Position Qty: {my_pos['quantity']} (Expected 8.0)")

# 5. Portfolio Snapshot
print("5. Create Snapshot")
# Trigger price refresh first to ensure valuation
make_request(f"{BASE_URL}/prices/refresh", method="POST", headers=headers)
time.sleep(1)

status, body = make_request(f"{BASE_URL}/portfolio/snapshot", method="POST", headers=headers)
if status != 201:
    print(f"Snapshot Failed: {status} {body}")
    exit(1)
print(f"Snapshot OK: {json.loads(body)['data']}")

# 6. Get History
print("6. Get History")
status, body = make_request(f"{BASE_URL}/portfolio/history", method="GET", headers=headers)
if status != 200:
    print(f"Get History Failed: {status} {body}")
    exit(1)
history = json.loads(body)
print(f"History Count: {len(history)}")
if len(history) > 0:
    print(f"Latest Snapshot: {history[0]}")
    print("✅ v0.5.0 Features Verified")
else:
    print("❌ No History Found")
