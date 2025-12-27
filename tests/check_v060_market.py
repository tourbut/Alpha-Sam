import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def make_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status >= 400:
                print(f"Request failed with status {response.status}")
                return None
            data = response.read()
            return json.loads(data)
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def check_search_symbol():
    print("Checking GET /market/search?q=AAPL ...")
    data = make_request("/market/search", {"q": "AAPL"})
    
    if data is None:
        return False
        
    # Expecting a list of results
    if not isinstance(data, list):
        print("FAILED: response is not a list")
        return False
        
    # Check for Apple in results
    found = False
    for item in data:
        # Adjust based on actual API response structure just in case
        # But expecting 'symbol' key based on previous code
        if isinstance(item, dict) and item.get("symbol") == "AAPL":
            found = True
            print(f"  Found AAPL: {item}")
            break
    
    if found:
        print("PASSED")
        return True
    else:
        print("FAILED: AAPL not found in results")
        return False

def check_validate_symbol():
    print("\nChecking GET /market/validate?symbol=BTC-USD ...")
    data = make_request("/market/validate", {"symbol": "BTC-USD"})
    
    if data is None:
        return False
        
    if data.get("valid") is True and data.get("symbol") == "BTC-USD":
        print(f"PASSED: {data}")
        return True
    else:
        print(f"FAILED: Unexpected response {data}")
        return False

def check_invalid_symbol():
    print("\nChecking GET /market/validate?symbol=INVALID_SYMBOL_XYZ ...")
    data = make_request("/market/validate", {"symbol": "INVALID_SYMBOL_XYZ"})
    
    if data is None:
        return False
        
    if data.get("valid") is False:
        print("PASSED: Correctly identified as invalid")
        return True
    else:
        print(f"FAILED: Should be invalid, got {data}")
        return False

if __name__ == "__main__":
    print(f"Targeting Backend at {BASE_URL}")
    
    results = [
        check_search_symbol(),
        check_validate_symbol(),
        check_invalid_symbol()
    ]
    
    if all(results):
        print("\nAll checks PASSED")
        sys.exit(0)
    else:
        print("\nSome checks FAILED")
        sys.exit(1)
