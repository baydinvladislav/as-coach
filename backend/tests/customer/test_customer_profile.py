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
