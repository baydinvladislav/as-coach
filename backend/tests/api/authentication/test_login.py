import pytest

from src.shared.config import TEST_COACH_USERNAME, TEST_COACH_PASSWORD
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_coach_login_successfully(create_coach, db):
    """Tests success user login on /api/login"""

    login_data = {
        "username": create_coach.username,
        "password": "qwerty123456",
        "fcm_token": "test fcm_token value",
    }

    response = await make_test_http_request("/api/login", "post", data=login_data)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("access_token") is not None
    assert response_json.get("refresh_token") is not None
    assert response_json.get("first_name") is not None
    assert response_json.get("user_type") == "coach"


@pytest.mark.asyncio
async def test_coach_login_failed(create_coach):
    """Login failed because such coach is not found"""

    login_data = {
        "username": "username_do_not_exist",
        "password": "some_password",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/login", "post", data=login_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_customer_login_by_otp_successfully(create_customer):
    """Tests success customer login by otp which created during customer creation"""

    login_data = {
        "username": create_customer.username,
        "password": create_customer.password,  # otp code
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/login", "post", create_customer.username, data=login_data)
    assert response.status_code == 200
