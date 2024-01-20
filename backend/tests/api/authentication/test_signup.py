import pytest

from sqlalchemy import select, delete

from src import Coach
from backend.tests.conftest import (
    make_test_http_request,
    TEST_COACH_FIRST_NAME,
    TEST_COACH_USERNAME,
    TEST_COACH_PASSWORD
)


@pytest.mark.asyncio
async def test_signup_successfully(override_get_db):
    """
    Success registration
    """
    user = await override_get_db.execute(
        select(Coach).where(Coach.username == TEST_COACH_USERNAME)
    )

    user_instance = user.scalar()
    if user_instance:
        await override_get_db.execute(
            delete(Coach).where(Coach.username == TEST_COACH_USERNAME)
        )
        await override_get_db.commit()

    signup_data = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME,
        "fcm_token": "test fcm token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_signup_validation_error(override_get_db):
    """
    Failed registration because of validation error
    """
    user = await override_get_db.execute(
        select(Coach).where(Coach.username == TEST_COACH_USERNAME)
    )

    user_instance = user.scalar()
    if user_instance:
        await override_get_db.execute(
            delete(Coach).where(Coach.username == TEST_COACH_USERNAME)
        )
        await override_get_db.commit()

    not_valid_signup_data = {
        # without "+"
        "username": "79850002233",
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME,
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_too_short_password(override_get_db):
    """
    Failed registration because of validation error
    """
    user = await override_get_db.execute(
        select(Coach).where(Coach.username == TEST_COACH_USERNAME)
    )

    user_instance = user.scalar()
    if user_instance:
        await override_get_db.execute(
            delete(Coach).where(Coach.username == TEST_COACH_USERNAME)
        )
        await override_get_db.commit()

    not_valid_signup_data = {
        "username": TEST_COACH_USERNAME,
        # password is less 8 symbols
        "password": "1234567",
        "first_name": TEST_COACH_FIRST_NAME,
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=not_valid_signup_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_failed_username_already_registered(create_user):
    """
    Failed because username already registered
    """
    signup_data = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME,
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/signup", "post", json=signup_data)
    assert response.status_code == 400
