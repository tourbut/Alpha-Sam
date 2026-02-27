import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.src.schemas.user import UserCreate
from app.src.crud.users import create_user
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_agent_docs():
    """
    Test GET /api/v1/agent/docs
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/agent/docs")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        first_doc = data[0]
        assert "method" in first_doc
        assert "url" in first_doc

@pytest.mark.asyncio
async def test_agent_login(test_session: AsyncSession):
    """
    Test POST /api/v1/agent/login
    """
    # 1. Create a test user
    test_user_in = UserCreate(
        email="agent_test@example.com",
        password="testpassword123!",
        nickname="Agent Test User",
    )
    user = await create_user(session=test_session, obj_in=test_user_in)
    
    # 2. Mock Dependency
    from app.src.core.db import get_session
    async def get_session_override():
        yield test_session
    app.dependency_overrides[get_session] = get_session_override

    # 3. Login via Agent API
    login_data = {
        "username": "agent_test@example.com",
        "password": "testpassword123!"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/agent/login", data=login_data)
        assert res.status_code == 200
        
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "api_docs" in data
        assert isinstance(data["api_docs"], list)
        assert "user" not in data
        
    app.dependency_overrides = {}
