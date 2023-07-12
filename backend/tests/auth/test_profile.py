import pytest
from httpx import AsyncClient

from src.auth.utils import create_access_token
from src.main import app


@pytest.mark.asyncio
async def test_get_user_profile(create_user):
    """
    Success GET user profile
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.get(
            "/api/profiles",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == create_user.username
    assert response.json()["first_name"] == create_user.first_name
    assert response.json()["user_type"] == "coach"


@pytest.mark.asyncio
async def test_post_user_profile(create_user):
    """
    Success updating user profile
    """
    prev_last_name = create_user.last_name

    update_user_data = {
        "first_name": create_user.first_name,
        "username": create_user.username,
        "last_name": prev_last_name[::-1],
        "email": "example@yandex.ru"
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.post(
            "/api/profiles",
            data=update_user_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["last_name"] != prev_last_name
    assert response.json()["last_name"] == update_user_data["last_name"]
    assert response.json()["email"] == update_user_data["email"]
    assert response.json()["user_type"] == "coach"
