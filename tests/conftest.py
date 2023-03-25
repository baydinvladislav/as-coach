import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from src.auth.models import User
from src.auth.utils import get_hashed_password
from src.main import app
from src.dependencies import get_db


TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
TEST_USER_LOGIN = os.environ.get("TEST_USER_LOGIN")
TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD")


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def create_user(session, client):
    """
    Fixture for creating test user
    """
    test_user_login = str(TEST_USER_LOGIN)
    test_user = session.query(User).filter(User.username == test_user_login).first()
    if test_user:
        return test_user

    test_user = User(
        username=test_user_login,
        password=get_hashed_password(TEST_USER_PASSWORD)
    )

    session.add(test_user)
    session.commit()

    return test_user
