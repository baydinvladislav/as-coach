import os

import pytest
from typing import Generator

from src.auth.models import User
from src.auth.utils import get_hashed_password
from src.main import app
from src.dependencies import get_db
from tests.dependencies import override_get_db, TestingSessionLocal


TEST_SIGNUP_USER_LOGIN = os.environ.get("TEST_SIGNUP_USER_LOGIN")
TEST_FIXTURE_USER_LOGIN = os.environ.get("TEST_FIXTURE_USER_LOGIN")
TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD")


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture()
def create_user(db):
    """
    Fixture for creating new application user
    """
    test_user_login = str(TEST_FIXTURE_USER_LOGIN)
    test_user = db.query(User).filter(User.username == test_user_login).first()
    if test_user:
        return test_user

    test_user = User(
        username=test_user_login,
        password=get_hashed_password(TEST_USER_PASSWORD)
    )

    db.add(test_user)
    db.commit()

    return test_user


@app.on_event("startup")
async def startup_event():
    app.dependency_overrides[get_db] = override_get_db
