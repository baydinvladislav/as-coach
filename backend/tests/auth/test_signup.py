import pytest
from httpx import AsyncClient

from src.auth.models import Coach
from src.main import app
from backend.tests.conftest import (
    TEST_COACH_FIRST_NAME, TEST_COACH_USERNAME, TEST_COACH_PASSWORD
)


@pytest.mark.anyio
async def test_signup_successfully(override_get_db):
    """
    Success registration
    """
    user = override_get_db.query(Coach).filter(
        Coach.username == TEST_COACH_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    body = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=body)

    assert response.status_code == 201


@pytest.mark.anyio
async def test_signup_validation_error(override_get_db):
    """
    Failed registration because of validation error
    """
    user = override_get_db.query(Coach).filter(
        Coach.username == TEST_COACH_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    body = {
        # without "+"
        "username": "79850002233",
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=body)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_signup_too_short_password(override_get_db):
    """
    Failed registration because of validation error
    """
    user = override_get_db.query(Coach).filter(
        Coach.username == TEST_COACH_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    signup_data = {
        "username": TEST_COACH_USERNAME,
        # password is less 8 symbols
        "password": "1234567",
        "first_name": TEST_COACH_FIRST_NAME
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=signup_data)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_signup_failed_username_already_registered(create_user):
    """
    Failed because username already registered
    """
    signup_data = {
        "username": TEST_COACH_USERNAME,
        "password": TEST_COACH_PASSWORD,
        "first_name": TEST_COACH_FIRST_NAME
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=signup_data)

    assert response.status_code == 400
