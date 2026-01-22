
import httpx
import asyncio
import sys

# Correct prefix based on main.py and api.py
# main.py includes api_router at /api/v1
# main.py includes fastapi_users register at /api/v1/auth/register
# main.py includes fastapi_users login at /api/v1/auth/jwt/login

BASE_URL = "http://127.0.0.1:8000/api/v1" 
EMAIL = "qa_test_001@example.com"
PASSWORD = "password123"

async def test_auth():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        print("1. Registering User...")
        try:
            # /api/v1/auth/signup
            resp = await client.post("/auth/signup", json={
                "email": EMAIL,
                "password": PASSWORD,
                "is_active": True,
                "is_superuser": False,
                "is_verified": False
            })
            if resp.status_code == 201:
                print(f"✅ Registration Success: {resp.json()}")
            elif resp.status_code == 400 and "already exists" in resp.text:
                 print(f"⚠️ User already exists, proceeding to login.")
            else:
                print(f"❌ Registration Failed: {resp.status_code} {resp.text}")
                # We expect 400 if user exists, so we proceed
                if resp.status_code != 400:
                    return
        except Exception as e:
             print(f"❌ Registration Error: {e}")

        print("\n2. Logging in...")
        try:
            # /api/v1/auth/login
            # Note: Custom auth.py uses JSON for login or Form data depending on implementation.
            # Base on code, it uses OAuth2PasswordRequestForm which expects form data.
            resp = await client.post("/auth/login", data={
                "username": EMAIL,
                "password": PASSWORD
            })
            
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("access_token")
                print(f"✅ Login Success. Token obtained: {token[:10]}...")
            else:
                print(f"❌ Login Failed: {resp.status_code} {resp.text}")
                return

        except Exception as e:
            print(f"❌ Login Error: {e}")
            return

        print("\n3. Testing Protected Route (/users/me)...")
        headers = {"Authorization": f"Bearer {token}"}
        # /api/v1/users/me
        resp = await client.get("/users/me", headers=headers)
        if resp.status_code == 200:
             print(f"✅ Protected Route Access Success: {resp.json()['email']}")
        else:
             print(f"❌ Protected Route Failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    try:
        asyncio.run(test_auth())
    except ImportError:
        print("Please install httpx")
