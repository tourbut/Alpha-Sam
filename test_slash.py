import requests

API_URL = "http://localhost:8000/api/v1"
EMAIL = "tester@example.com"
PASSWORD = "password123"

def test_transactions():
    # 1. Login
    login_url = f"{API_URL}/auth/login"
    data = {"username": EMAIL, "password": PASSWORD}
    print(f"Logging in to {login_url}...")
    try:
        resp = requests.post(login_url, data=data)
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return
        token = resp.json()["access_token"]
        print("Login successful.")
    except Exception as e:
        print(f"Login error: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test NO Slash
    url_no_slash = f"{API_URL}/transactions"
    print(f"\nTesting GET {url_no_slash}")
    resp_no_slash = requests.get(url_no_slash, headers=headers, allow_redirects=False)
    print(f"Status: {resp_no_slash.status_code}")
    if resp_no_slash.status_code == 307:
        print(f"Redirect Location: {resp_no_slash.headers.get('Location')}")
    
    # 3. Test WITH Slash
    url_slash = f"{API_URL}/transactions/"
    print(f"\nTesting GET {url_slash}")
    resp_slash = requests.get(url_slash, headers=headers)
    print(f"Status: {resp_slash.status_code}")
    print(f"Response: {resp_slash.text[:100]}...")

if __name__ == "__main__":
    test_transactions()
