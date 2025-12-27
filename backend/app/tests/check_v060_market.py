import urllib.request
import urllib.parse
import json
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

def make_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    print(f"Request: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            if response.status >= 400:
                print(f"FAILED: Status {response.status}")
                return None
            data = response.read()
            return json.loads(data)
    except Exception as e:
        print(f"FAILED: Connection Error: {e}")
        return None

def check_search_symbol():
    print("\n[Test] Search Symbol 'AAPL'")
    data = make_request("/market/search", {"q": "AAPL"})
    
    if data is None:
        return False
        
    if not isinstance(data, list):
        print(f"FAILED: Expected list, got {type(data)}")
        return False
        
    for item in data:
        # Check for expected structure
        if "symbol" in item and item["symbol"] == "AAPL":
            print(f"PASSED: Found AAPL ({item.get('name')})")
            return True
            
    print("FAILED: AAPL not found in results")
    return False

def check_validate_symbol():
    print("\n[Test] Validate Symbol 'BTC-USD'")
    data = make_request("/market/validate", {"symbol": "BTC-USD"})
    
    if data and data.get("valid") is True:
        print(f"PASSED: Validated BTC-USD")
        return True
    else:
        print(f"FAILED: Could not validate BTC-USD. Response: {data}")
        return False

def check_validate_invalid():
    print("\n[Test] Validate Invalid Symbol 'INVALID_XYZ_123'")
    data = make_request("/market/validate", {"symbol": "INVALID_XYZ_123"})
    
    if data and data.get("valid") is False:
        print(f"PASSED: Correctly identified as invalid")
        return True
    else:
        print(f"FAILED: Should be invalid. Response: {data}")
        return False

if __name__ == "__main__":
    print(f"Running v0.6.0 Market Data Tests against {BASE_URL}")
    
    tests = [
        check_search_symbol(),
        check_validate_symbol(),
        check_validate_invalid()
    ]
    
    if all(tests):
        print("\nAll Backend Tests PASSED ✅")
        sys.exit(0)
    else:
        print("\nSome Backend Tests FAILED ❌")
        sys.exit(1)
