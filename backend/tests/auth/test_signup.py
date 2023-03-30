import pytest
from httpx import AsyncClient

from src.auth.models import User
from src.main import app
from backend.tests.conftest import TEST_USER_PASSWORD, TEST_USER_USERNAME


@pytest.mark.anyio
async def test_signup_successfully(override_get_db):
    """
    Success registration
    """
    user = override_get_db.query(User).filter(
        User.username == TEST_USER_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    body = {
        "username": TEST_USER_USERNAME,
        "password": TEST_USER_PASSWORD
    }

    print(TEST_USER_USERNAME)
    print(TEST_USER_PASSWORD)

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=body)

    assert response.status_code == 201


@pytest.mark.anyio
async def test_signup_validation_error(override_get_db):
    """
    Failed registration because of validation error
    """
    user = override_get_db.query(User).filter(
        User.username == TEST_USER_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    body = {
        # without "+"
        "username": "79850002233",
        "password": TEST_USER_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=body)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_signup_too_short_password(override_get_db):
    """
    Failed registration because of validation error
    """
    user = override_get_db.query(User).filter(
        User.username == TEST_USER_USERNAME
    ).first()

    if user:
        override_get_db.delete(user)
        override_get_db.commit()

    signup_data = {
        "username": TEST_USER_USERNAME,
        # password is less 8 symbols
        "password": "1234567"
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
        "username": TEST_USER_USERNAME,
        "password": TEST_USER_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/api/signup", json=signup_data)

    assert response.status_code == 400
