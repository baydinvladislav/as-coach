import pytest

from backend.tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_signup_successfully(db):
    """Success registration"""

    signup_data = {
        "username": "+79031234567",
        "password": "qwerty123",
        "first_name": "Ivan",
        "fcm_token": "test fcm token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 201

    response_json = response.json()

    assert response_json.get("access_token") is not None
    assert response_json.get("refresh_token") is not None
    assert response_json.get("username") == signup_data.get("username")
    assert response_json.get("first_name") == signup_data.get("first_name")


@pytest.mark.asyncio
async def test_signup_validation_error(db):
    """Failed registration because of validation error"""

    not_valid_signup_data = {
        "username": "79850002233",  # without "+"
        "password": "qwerty123",
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_too_short_password(db):
    """Failed registration because of validation error"""

    not_valid_signup_data = {
        "username": "79850002233",
        "password": "1234567",  # password is less 8 symbols
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_failed_username_already_registered(create_coach):
    """Failed because username already registered"""

    signup_data = {
        "username": create_coach.username,
        "password": "qwerty123456",
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 400
