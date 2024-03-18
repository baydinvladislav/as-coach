from httpx import AsyncClient, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src import engine
from src.utils import create_access_token
from src.shared.dependencies import get_db
from src.main import app
from tests.fixtures import *
from tests.mocks import *

TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def make_test_http_request(
        url: str,
        method: str,
        username: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
) -> Response:
    """
    Make tests http request to server,
    has username if test case requires authed user.

    Args:
        url: testing endpoint
        method: http request method
        username: authed user who makes http request
        data: data sent to server
        json: data to signup
    """
    headers = None
    if username:
        auth_token = await create_access_token(username)
        headers = dict()
        headers["Authorization"] = f"Bearer {auth_token}"

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        match method:
            case "get":
                response = await ac.get(url, headers=headers)
            case "post":
                kwargs = {"headers": headers, "data": data, "json": json}
                response = await ac.post(url, **{key: val for key, val in kwargs.items() if val})
            case _:
                raise ValueError("Unexpected method")

        return response


@app.on_event("startup")
async def startup_event():
    """
    In the beginning on each test creates database schema,
    also changes production db to testing db
    """
    from src import Base, engine

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
