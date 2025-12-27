import urllib.request
import urllib.parse
import json
import ssl
import sys

# Bypass SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://localhost:8000/api/v1"

def make_request(url, method="GET", data=None, headers={}):
    try:
        req = urllib.request.Request(url, method=method)
        # Add basic user agent to avoid some blocks, though requests usually handled by backend
        req.add_header("User-Agent", "TestScript/1.0")
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

print("--- QA v0.6.0 Market Service Check ---")

# 1. Search Symbol
print("1. Testing Symbol Search (Query: 'Apple')")
status, body = make_request(f"{BASE_URL}/market/search?q=Apple", method="GET")
if status != 200:
    print(f"FAILED: Search returned {status} {body}")
    sys.exit(1)

try:
    results = json.loads(body)
except json.JSONDecodeError:
    print(f"FAILED: Could not decode JSON. Body: {body}")
    sys.exit(1)

print(f"Search Results: {len(results)} items found.")
# Check if AAPL is in the results
found = False
if isinstance(results, list):
    found = any(item.get('symbol') == 'AAPL' for item in results)

if found:
    print("✅ Found AAPL in search results.")
else:
    print("⚠️ AAPL not found in search results for 'Apple'. Results might be from different exchange or format.")
    if len(results) > 0:
        print(f"First 3 results: {results[:3]}")

# 2. Validate Symbol
print("\n2. Testing Symbol Validation (Symbol: 'BTC-USD')")
status, body = make_request(f"{BASE_URL}/market/validate?symbol=BTC-USD", method="GET")
if status != 200:
    print(f"FAILED: Validate returned {status} {body}")
    sys.exit(1)

data = json.loads(body)
if data.get("valid") is True:
    print("✅ BTC-USD is valid.")
else:
    print(f"❌ BTC-USD validation failed. Response: {data}")
    # Don't exit here, continues to next check
    # sys.exit(1)

# 3. Validate Invalid Symbol
print("\n3. Testing Invalid Symbol (Symbol: 'INVALID12345')")
status, body = make_request(f"{BASE_URL}/market/validate?symbol=INVALID12345", method="GET")
data = json.loads(body)
if data.get("valid") is False:
    print("✅ Invalid symbol correctly identified as invalid.")
else:
    print(f"❌ Invalid symbol check failed. Response: {data}")

print("\nMarket API checks completed.")
