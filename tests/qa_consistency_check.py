import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "qa_auto_v1@example.com"
PASSWORD = "password123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_backend():
    session = requests.Session()
    
    # 1. Signup (Ignore if exists)
    try:
        r = session.post(f"{BASE_URL}/auth/signup", json={"email": EMAIL, "password": PASSWORD})
        if r.status_code == 201:
            log("User registered.", "PASS")
        elif r.status_code == 400 and "already exists" in r.text:
            log("User already exists.", "SKIP")
        else:
            log(f"Register failed: {r.status_code} {r.text}", "FAIL")
    except Exception as e:
        log(f"Register error: {e}", "FAIL")

    # 2. Login
    try:
        r = session.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
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

        # 5.1 Create Transaction (Multi-portfolio version)
        # First, find a portfolio or use a default one. 
        # For simplicity, we get the list and use the first one, or create one.
        r_port = session.get(f"{BASE_URL}/portfolios")
        if r_port.status_code == 200 and r_port.json():
            portfolio_id = r_port.json()[0]["id"]
            log(f"Using portfolio {portfolio_id} for transactions.", "INFO")
        else:
            # Create a default portfolio if none exists
            r_port = session.post(f"{BASE_URL}/portfolios", json={"name": "QA Portfolio", "description": "Auto generated"})
            portfolio_id = r_port.json()["id"]
            log(f"Created new portfolio {portfolio_id}.", "PASS")

        transaction_data = {
            "asset_id": asset_id,
            "type": "BUY",
            "quantity": 10.0,
            "price": 100.0,
            "executed_at": "2026-01-18T10:00:00"
        }
        # Correct path: /portfolios/{id}/transactions
        r = session.post(f"{BASE_URL}/portfolios/{portfolio_id}/transactions", json=transaction_data)
        if r.status_code == 201:
            log(f"POST /portfolios/{{id}}/transactions (Create): {r.status_code}", "PASS")
        else:
            log(f"POST /portfolios/{{id}}/transactions (Create): {r.status_code} {r.text}", "FAIL")
        
        # 6. Delete Asset
        r = session.delete(f"{BASE_URL}/assets/{asset_id}")
        log(f"DELETE /assets/{{id}}: {r.status_code}", "PASS" if r.status_code == 204 else "FAIL")
    elif r.status_code == 400: # Already exists maybe
        log(f"POST /assets/ (Create): {r.status_code} (Likely exists)", "WARN")
    else:
        log(f"POST /assets/ (Create): {r.status_code}", "FAIL")

    # 7. Portfolio Summary
    r = session.get(f"{BASE_URL}/portfolios/summary")
    log(f"GET /portfolios/summary: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

    # 8. Portfolio History
    r = session.get(f"{BASE_URL}/portfolios/history")
    log(f"GET /portfolios/history: {r.status_code}", "PASS" if r.status_code == 200 else "FAIL")

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
