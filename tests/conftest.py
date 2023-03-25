import os

from src.dependencies import get_db
from src.main import app


DATABASE_URL = os.getenv("DATABASE_URL")
TEST_USER_USERNAME = "+79856352655"
TEST_USER_PASSWORD = "my_test_pswd"


@app.on_event("startup")
async def startup_event():
    from tests.tests import engine, override_get_db
    from database import Base

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
