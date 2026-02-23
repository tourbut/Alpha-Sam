import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.src.core.db import AsyncSessionLocal
from app.src.models.user import User
from sqlalchemy import select, delete

@pytest.mark.asyncio
async def test_x_user_id_header_isolation():
    """
    X-User-Id 헤더를 통한 사용자 격리 테스트
    """
    import uuid
    uid1 = uuid.uuid4()
    uid2 = uuid.uuid4()
    
    # 0. 테스트용 사용자 생성 (만약 없으면)
    async with AsyncSessionLocal() as session:
        for uid in [uid1, uid2]:
            stmt = select(User).where(User.id == uid)
            result = await session.execute(stmt)
            if not result.scalar_one_or_none():
                user = User(id=uid, email=f"test{uid}@example.com", hashed_password="path", is_active=True)
                session.add(user)
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. User uid1로 설정 조회 (없으면 자동 생성됨)
        response = await client.get("/api/v1/users/me/settings", headers={"X-User-Id": str(uid1)})
        assert response.status_code == 200
        data1 = response.json()
        assert data1["user_id"] == str(uid1)
        
        # 2. User uid1 설정 업데이트
        update_data = {"daily_report_enabled": False, "price_alert_enabled": False}
        response = await client.post("/api/v1/users/me/settings", json=update_data, headers={"X-User-Id": str(uid1)})
        assert response.status_code == 200
        assert response.json()["daily_report_enabled"] is False
        
        # 3. User uid2로 설정 조회 (User uid1와 달라야 함)
        response = await client.get("/api/v1/users/me/settings", headers={"X-User-Id": str(uid2)})
        assert response.status_code == 200
        data2 = response.json()
        assert data2["user_id"] == str(uid2)
        assert data2["daily_report_enabled"] is True # 기본값
