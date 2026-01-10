import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "qa_auto_v1@example.com"
PASSWORD = "password123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_backend():
    session = requests.Session()
    
    # 1. Register (Ignore if exists)
    try:
        r = session.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD})
        if r.status_code == 201:
            log("User registered.", "PASS")
        elif r.status_code == 400 and "REGISTER_USER_ALREADY_EXISTS" in r.text:
            log("User already exists.", "SKIP")
        else:
            log(f"Register failed: {r.status_code} {r.text}", "FAIL")
    except Exception as e:
        log(f"Register error: {e}", "FAIL")

    # 2. Login
    try:
        r = session.post(f"{BASE_URL}/auth/jwt/login", data={"username": EMAIL, "password": PASSWORD})
        if r.status_code in [200, 204]:
            token = r.json().get("access_token")
            session.headers.update({"Authorization": f"Bearer {token}"})
            log("Login successful.", "PASS")
        else:
            log(f"Login failed: {r.status_code} {r.text}", "FAIL")
            return
    except Exception as e:
        log(f"Login error: {e}", "FAIL")
        return

    # 3. Test Users Me
    r = session.get(f"{BASE_URL}/users/me")
    log(f"GET /users/me: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

    # 4. Test Assets (List)
    r = session.get(f"{BASE_URL}/assets/")
    log(f"GET /assets/: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

    # 5. Create Asset (Unit Test)
    asset_data = {"symbol": "QA-COIN", "name": "QA Coin", "category": "Crypto"}
    r = session.post(f"{BASE_URL}/assets/", json=asset_data)
    if r.status_code == 201:
        asset_id = r.json()["id"]
        log(f"POST /assets/ (Create): {r.status_code}", "PASS")

        # 5.1 Create Position
        position_data = {"asset_id": asset_id, "quantity": 10, "buy_price": 100.0}
        r = session.post(f"{BASE_URL}/positions/", json=position_data)
        if r.status_code == 201:
            log(f"POST /positions/ (Create): {r.status_code}", "PASS")
            pos_id = r.json()["id"]
            
            # 5.2 Delete Position
            r = session.delete(f"{BASE_URL}/positions/{pos_id}")
            log(f"DELETE /positions/{{id}}: {r.status_code}", "PASS" if r.status_code == 204 else "FAIL")
            
        else:
            log(f"POST /positions/ (Create): {r.status_code} {r.text}", "FAIL")
        
        # 6. Delete Asset
        r = session.delete(f"{BASE_URL}/assets/{asset_id}")
        log(f"DELETE /assets/{{id}}: {r.status_code}", "PASS" if r.status_code == 204 else "FAIL")
    elif r.status_code == 400: # Already exists maybe
        log(f"POST /assets/ (Create): {r.status_code} (Likely exists)", "WARN")
    else:
        log(f"POST /assets/ (Create): {r.status_code}", "FAIL")

    # 7. Portfolio Summary
    r = session.get(f"{BASE_URL}/portfolio/summary")
    log(f"GET /portfolio/summary: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

    # 8. Portfolio History
    r = session.get(f"{BASE_URL}/portfolio/history")
    log(f"GET /portfolio/history: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

    # 9. Market Search
    r = session.get(f"{BASE_URL}/market/search?q=BTC")
    log(f"GET /market/search: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")
    
    # 10. Settings
    r = session.get(f"{BASE_URL}/users/me/settings")
    log(f"GET /users/me/settings: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

if __name__ == "__main__":
    try:
        test_backend()
    except Exception as e:
        print(f"Critical Error: {e}")
