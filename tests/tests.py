import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.anyio
async def test_root(override_get_db):
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
