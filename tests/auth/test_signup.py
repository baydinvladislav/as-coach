import pytest
from httpx import AsyncClient

from auth.models import User
from main import app
from tests.conftest import TEST_USER_PASSWORD, TEST_USER_USERNAME


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

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/signup", json=body)

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
        response = await ac.post("/signup", json=body)

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

    body = {
        "username": TEST_USER_USERNAME,
        # password is less 8 symbols
        "password": "1234567"
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post("/signup", json=body)

    assert response.status_code == 422
