from httpx import AsyncClient, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src import engine
from src.utils import create_access_token
from tests.fixtures import (
    db,
    db_engine,
    client,
    create_coach,
    create_customer,
    create_muscle_groups,
    create_exercises,
    create_training_plans,
    create_trainings,
    create_training_exercises,
)
from tests.mocks import mock_send_kafka_message, mock_send_push_notification

TestingSessionLocal = sessionmaker(
    engine, autocommit=False, expire_on_commit=False, autoflush=False, class_=AsyncSession
)


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
