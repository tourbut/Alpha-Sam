import urllib.request
import urllib.parse
import json
import secrets
import ssl

# Bypass SSL if needed (localhost)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = f"qa_{secrets.token_hex(4)}@test.com"
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

# 1. Signup
print(f"Signup: {EMAIL}")
status, body = make_request(f"{BASE_URL}/auth/signup", method="POST", data={"email": EMAIL, "password": PASSWORD, "nickname": "qatest"})
print(f"Signup Status: {status}")
print(f"Signup Body: {body}")

# 2. Login
print("Login...")
status, body = login(EMAIL, PASSWORD)
print(f"Login Status: {status}")
# print(f"Login Body: {body}")
token = None
if status == 200:
    data = json.loads(body)
    token = data.get("access_token")
    print("Login Token:", token[:10] + "..." if token else "None")

if token:
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Asset
    print("Create Asset...")
    asset_data = {"name": "QA Asset", "symbol": f"QA{secrets.token_hex(2)}", "asset_type": "Stock", "sector": "Tech"}
    status, body = make_request(f"{BASE_URL}/assets/", method="POST", data=asset_data, headers=headers)
    print(f"Create Asset Status: {status}")
    print(f"Create Asset Body: {body}")
        
    # 4. List Assets
    print("List Assets...")
    status, body = make_request(f"{BASE_URL}/assets/", method="GET", headers=headers)
    print(f"List Assets Status: {status}")
    if status == 200:
        assets = json.loads(body)
        print(f"List Assets Count: {len(assets)}")
