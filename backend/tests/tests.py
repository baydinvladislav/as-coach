import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
