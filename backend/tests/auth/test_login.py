import pytest
from httpx import AsyncClient

from src.auth.utils import get_hashed_password
from src.auth.models import Coach
from src.main import app
from backend.tests.conftest import (
    TEST_USER_FIRST_NAME, TEST_USER_USERNAME, TEST_USER_PASSWORD
)


@pytest.mark.anyio
async def test_login_successfully(override_get_db):
    """
    Tests success user login
    """
    user = override_get_db.query(Coach).filter(
        Coach.username == TEST_USER_USERNAME
    ).first()

    if not user:
        user = Coach(
            username=TEST_USER_USERNAME,
            first_name=TEST_USER_FIRST_NAME,
            password=get_hashed_password(TEST_USER_PASSWORD)
        )

        override_get_db.add(user)
        override_get_db.commit()

    login_data = {
        "username": TEST_USER_USERNAME,
        "password": TEST_USER_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post(
            "/api/login",
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_login_failed():
    """
    Failed because user is not found
    """
    login_data = {
        "username": "username_do_not_exist",
        "first_name": TEST_USER_FIRST_NAME,
        "password": TEST_USER_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post(
            "/api/login",
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 404
