import pytest
from httpx import AsyncClient

from src.main import app
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_customer_get_profile(create_customer, override_get_db):
    """
    Tests that customer can get profile on /api/profiles
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.username)
        response = await ac.get(
            "/api/profiles",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["user_type"] == "customer"


@pytest.mark.anyio
async def test_customer_update_profile(create_customer, override_get_db):
    """
    Tests that customer can update profile on /api/profiles
    """
    updated_profile = {
        "username": create_customer.username,
        "first_name": create_customer.first_name,
        "email": "newemail@gmail.com",
        "last_name": "Petrov"
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.username)
        response = await ac.post(
            "/api/profiles",
            data=updated_profile,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["email"] == updated_profile["email"]
    assert response.json()["last_name"] == updated_profile["last_name"]
    assert response.json()["user_type"] == "customer"
