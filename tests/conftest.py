import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.dependencies import get_db
from src.main import app


DATABASE_URL = os.getenv("DATABASE_URL")
TEST_USER_USERNAME = os.getenv("TEST_USER_USERNAME")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def override_get_db():
    """
    Creates session to testing db
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """
    In the beginning on each test creates database schema,
    also changes production db to testing db
    """
    from database import Base

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
