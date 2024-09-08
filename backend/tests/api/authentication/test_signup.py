import pytest

from backend.tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_signup_successfully():
    """
    Success registration
    """
    signup_data = {
        "username": "+79031234567",
        "password": "qwerty123",
        "first_name": "Ivan",
        "fcm_token": "test fcm token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_signup_validation_error():
    """
    Failed registration because of validation error
    """
    not_valid_signup_data = {
        # without "+"
        "username": "79850002233",
        "password": "qwerty123",
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_too_short_password():
    """
    Failed registration because of validation error
    """
    not_valid_signup_data = {
        "username": "79850002233",
        # password is less 8 symbols
        "password": "1234567",
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_failed_username_already_registered(create_coach):
    """
    Failed because username already registered
    """
    signup_data = {
        "username": create_coach.username,
        "password": "qwerty123456",
        "first_name": "Ivan",
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 400
