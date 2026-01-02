import urllib.request
import urllib.parse
import json
import secrets
import ssl
import time
import sys

# Bypass SSL if needed (localhost)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = f"qa_portfolio_{secrets.token_hex(4)}@test.com"
PASSWORD = "password123"

def make_request(url, method="GET", data=None, headers={}, expected_status=None):
    req = urllib.request.Request(url, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    
    if data:
        json_data = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
        req.data = json_data
        
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            status_code = response.status
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        status_code = e.code
        body = e.read().decode("utf-8")
    except Exception as e:
        print(f"Error requesting {url}: {e}")
        return 0, str(e)

    if expected_status and status_code != expected_status:
        print(f"FAILED: {method} {url} returned {status_code}, expected {expected_status}")
        print(f"Body: {body}")
        sys.exit(1)
        
    return status_code, body

def login(email, password):
    url = f"{BASE_URL}/auth/login"
    data = urllib.parse.urlencode({"username": email, "password": password}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")

# 1. Signup
print(f"1. Signup: {EMAIL}")
make_request(f"{BASE_URL}/auth/register", method="POST", data={"email": EMAIL, "password": PASSWORD, "nickname": "portfolio_tester"}, expected_status=201)

# 2. Login
print("2. Login...")
# Login path is /auth/jwt/login and it uses form data for username/password, usually, or json depending on config.
# FastAPI Users default /jwt/login often uses application/x-www-form-urlencoded (OAuth2 standard)
# But standard json login might be available if configured?
# Let's try standard form data login first as per check_api.py (which used form data encoding)
# But path is /auth/jwt/login
def login(email, password):
    url = f"{BASE_URL}/auth/jwt/login"
    data = urllib.parse.urlencode({"username": email, "password": password}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")

status, body = login(EMAIL, PASSWORD)
if status != 200:
    print(f"Login failed: {status} {body}")
    sys.exit(1)

data = json.loads(body)
token = data.get("access_token")
headers = {"Authorization": f"Bearer {token}"}
print("   Login successful")

# 3. Create Asset
print("3. Create Asset...")
asset_symbol = f"PF{secrets.token_hex(2)}"
asset_data = {"name": "Portfolio Test Asset", "symbol": asset_symbol, "asset_type": "Stock", "sector": "Tech"}
status, body = make_request(f"{BASE_URL}/assets/", method="POST", data=asset_data, headers=headers, expected_status=201)
asset = json.loads(body)
asset_id = asset["id"]
print(f"   Asset created: {asset_symbol} (ID: {asset_id})")

# 4. Create Position
print("4. Create Position...")
position_data = {
    "asset_id": asset_id,
    "quantity": 10.0,
    "buy_price": 100.0,
    "buy_date": "2025-01-01"
}
make_request(f"{BASE_URL}/positions/", method="POST", data=position_data, headers=headers, expected_status=201)
print("   Position created")

# 5. Get Portfolio Summary
print("5. Get Portfolio Summary...")
start_time = time.time()
# Note: route prefix is /portfolio (singular) based on api.py
status, body = make_request(f"{BASE_URL}/portfolio/summary", method="GET", headers=headers, expected_status=200)
end_time = time.time()
duration = end_time - start_time

print(f"   Portfolio Summary retrieved in {duration:.4f} seconds")
summary_data = json.loads(body)

# Validation
positions = summary_data.get("positions", [])
if len(positions) != 1:
    print(f"FAILED: Expected 1 position, got {len(positions)}")
    sys.exit(1)

pos = positions[0]
if pos["asset_symbol"] != asset_symbol:
    print(f"FAILED: Expected asset symbol {asset_symbol}, got {pos.get('asset_symbol')}")
    sys.exit(1)

if pos["quantity"] != 10.0:
    print(f"FAILED: Expected quantity 10.0, got {pos['quantity']}")
    sys.exit(1)

print("SUCCESS: Portfolio Summary verification passed!")
