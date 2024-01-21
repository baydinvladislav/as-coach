import pytest

from tests.conftest import (
    make_test_http_request,
)
from src.config import TEST_COACH_FIRST_NAME, TEST_COACH_USERNAME, TEST_COACH_PASSWORD


@pytest.mark.asyncio
async def test_login_successfully(create_user, override_get_db):
    """
    Tests success user login on /api/login
    Checks tokens in the response
    """
    # test user is "registered" by fixture
    login_data = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD,
        "fcm_token": "test fcm_token value",
    }

    response = await make_test_http_request("/api/login", "post", data=login_data)
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data


@pytest.mark.asyncio
async def test_login_failed():
    """
    Failed because user is not found
    """
    login_data = {
        "username": "username_do_not_exist",
        "first_name": TEST_COACH_FIRST_NAME,
        "password": TEST_COACH_PASSWORD,
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/login", "post", data=login_data)
    assert response.status_code == 404
