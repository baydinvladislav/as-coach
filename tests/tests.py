import os
import pytest

from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.auth.models import User


DATABASE_URL = os.getenv("DATABASE_URL")
TEST_USER_USERNAME = "+79856352655"
TEST_USER_PASSWORD = "my_test_pswd"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.mark.anyio
async def test_root(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_successfully_signup(override_get_db):
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

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/signup", json=body)

    assert response.status_code == 201
