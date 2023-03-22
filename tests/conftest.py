import pytest
from typing import Generator

from src.auth.models import User
from src.auth.utils import get_hashed_password
from src.main import app
from src.dependencies import get_db
from tests.dependencies import override_get_db, TestingSessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture()
def create_user(db):
    test_user_name = "+79857994488"
    test_user = db.query(User).filter(User.username == test_user_name).first()
    if test_user:
        return test_user

    test_user = User(
        username=test_user_name,
        password=get_hashed_password("my_test_pswd")
    )

    db.add(test_user)
    db.commit()

    return test_user


@app.on_event("startup")
async def startup_event():
    app.dependency_overrides[get_db] = override_get_db
