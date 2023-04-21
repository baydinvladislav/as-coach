import pytest
from httpx import AsyncClient

from src.main import app
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_coach_get_me(create_user, override_get_db):
    """
    Tests that coach can get response from /api/me
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.get(
            "/api/me",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["user_type"] == "coach"
