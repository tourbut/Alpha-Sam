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
EMAIL = f"qa_script_{secrets.token_hex(4)}@test.com"
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

print(f"--- QA Script: {EMAIL} ---")

# 1. Signup
print("1. Signup")
status, body = make_request(f"{BASE_URL}/auth/signup", method="POST", data={"email": EMAIL, "password": PASSWORD, "nickname": "OriginalNick"})
if status != 201:
    print(f"Signup Failed: {status} {body}") # Might fail if email collision (unlikely with hex)
    # create another one?
    # proceed if already exists? No, login needs pass.
    # checking status 400
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

# 3. Test Price API
print("3. Test Price API (AAPL & BTC-USD)")

for ticker in ["AAPL", "BTC-USD"]:
    print(f"Checking {ticker}...")
    asset_data = {"name": f"Test {ticker}", "symbol": ticker, "asset_type": "Stock", "sector": "Tech"}
    status, body = make_request(f"{BASE_URL}/assets/", method="POST", data=asset_data, headers=headers)
    
    if status == 201:
        print(f"Created {ticker}")
    elif status == 400 and "already exists" in body:
        print(f"{ticker} already exists, proceeding to check price")
    else:
        print(f"Create Failed: {status} {body}")

print("Waiting 3s...")
time.sleep(3)

# List Assets
status, body = make_request(f"{BASE_URL}/assets/", method="GET", headers=headers)
if status == 200:
    assets = json.loads(body)
    for ticker in ["AAPL", "BTC-USD"]:
        target = next((a for a in assets if a["symbol"] == ticker), None)
        if target:
            price = target.get("latest_price")
            print(f"[{ticker}] Price: {price}")
            if price and price > 0:
                print(f"✅ {ticker} Success")
            else:
                print(f"❌ {ticker} Failed (Null/Zero)")
        else:
            print(f"Warning: {ticker} not found in user list (maybe owned by another user?)")
            # Note: The API design implies assets are GLOBAL or USER-specific? 
            # If User-specific, "already exists" implies global uniqueness or collision in user scope.
            # "Asset with symbol AAPL already exists" usually means Global Uniqueness in DB.
            # But GET /assets might only return USER assets?
            # Or GET /assets returns ALL assets?
            # Let's check logic.
else:
    print(f"List Assets Failed: {status} {body}")
