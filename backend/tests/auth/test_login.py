import pytest
from httpx import AsyncClient

from src.main import app
from backend.tests.conftest import (
    TEST_COACH_FIRST_NAME,
    TEST_COACH_USERNAME,
    TEST_COACH_PASSWORD
)


@pytest.mark.asyncio
async def test_login_successfully(create_user, override_get_db):
    """
    Tests success user login on /api/login
    Checks tokens in the response
    """

    # test user is created by fixture
    login_data = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post(
            "/api/login",
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 200

    response = response.json()
    assert "access_token" in response
    assert "refresh_token" in response


@pytest.mark.asyncio
async def test_login_failed():
    """
    Failed because user is not found
    """

    login_data = {
        "username": "username_do_not_exist",
        "first_name": TEST_COACH_FIRST_NAME,
        "password": TEST_COACH_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post(
            "/api/login",
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 404
