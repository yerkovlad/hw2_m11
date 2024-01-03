import httpx
import pytest
from your_project.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        data = {"email": "test@example.com", "password": "password123", "name": "Test User"}
        response = await client.post("/users/", json=data)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
