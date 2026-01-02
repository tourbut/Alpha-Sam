import asyncio
import sys
import os
import uuid


# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.src.core.db import AsyncSessionLocal
from sqlalchemy import text

BASE_URL = "http://127.0.0.1:8000/api/v1"

async def verify_legacy_data_in_db():
    print("\n🔍 [1/2] Verifying Legacy Data in DB...")
    async with AsyncSessionLocal() as session:
        # Check if legacy position exists and has owner_id=1
        stmt = text("""
            SELECT p.id, p.owner_id 
            FROM positions p
            JOIN assets a ON p.asset_id = a.id
            WHERE a.symbol = 'LEGACY_POS_ASSET'
        """)
        result = await session.execute(stmt)
        row = result.first()
        
        if not row:
            print("⚠️ Legacy Asset/Position not found. Did you run `qa_generate_dirty_data_v090.py`?")
            # If dirty data wasn't created, we can't verify migration of IT. 
            # But if this is production verify, skipping might be okay if we assume migration ran on real data.
            # However, for this workflow, we want to see PASS.
            return False

        print(f"   Found Legacy Position ID={row.id}, OwnerID={row.owner_id}")
        
        if row.owner_id == 1:
            print("✅ Legacy Data Verification PASSED: owner_id is 1.")
            return True
        else:
            print(f"❌ Legacy Data Verification FAILED: owner_id is {row.owner_id}, expected 1.")
            return False

import json
import urllib.request
import urllib.error

async def smoke_test_api():
    print("\n🚀 [2/2] Running API Smoke Test (urllib)...")
    new_email = f"qa_verif_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    
    # helper for requests
    def make_request(endpoint, method="GET", data=None, headers=None):
        url = f"{BASE_URL}{endpoint}"
        req = urllib.request.Request(url, method=method)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        if data:
            json_data = json.dumps(data).encode("utf-8")
            req.add_header("Content-Type", "application/json")
            req.data = json_data
            
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())
        except Exception as e:
            print(f"Request Error: {e}")
            return 500, str(e)

    # 1. Register
    print(f"   Registering {new_email}...")
    status, body = make_request("/auth/register", "POST", {
        "email": new_email,
        "password": password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    })
    
    if status not in [201, 400]:
        print(f"❌ Registration Failed: {status} {body}")
        return False

    # 2. Login
    print("   Logging in...")
    # Login usually expects form-data or json depending on config. verify_snapshot used data.
    # But standard fastapi-users /login often uses x-www-form-urlencoded or json.
    # qa_auth_api.py used data={"username":..., "password":...} which httpx sends as form.
    # urllib needs manual encoding for form data.
    
    login_data = urllib.parse.urlencode({
        "username": new_email,
        "password": password
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(f"{BASE_URL}/auth/jwt/login", data=login_data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        status = e.code
        body = json.loads(e.read().decode())

    if status != 200:
        print(f"❌ Login Failed: {status} {body}")
        return False
    
    token = body.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login Successful.")

    # 3. Get Me
    status, body = make_request("/users/me", "GET", headers=headers)
    if status != 200:
        print(f"❌ Get Profile Failed: {status} {body}")
        return False
    user_id = body.get("id")
    print(f"   User Profile Verified. ID={user_id}")
    
    print("✅ API Smoke Test PASSED.")
    return True

async def main():
    print("=== v0.9.0 Production Verification Script ===")
    
    # 1. DB Check
    db_pass = await verify_legacy_data_in_db()
    
    # 2. API Check
    api_pass = await smoke_test_api()
    
    if db_pass and api_pass:
        print("\n🎉 ALL CHECKS PASSED. Ready for sign-off.")
        sys.exit(0)
    else:
        print("\n⚠️ SOME CHECKS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
