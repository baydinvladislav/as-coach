import pytest

from httpx import AsyncClient

from src.main import app
from src.auth.utils import create_access_token


@pytest.mark.asyncio
async def test_get_all_muscle_groups(
    create_user,
    create_exercises,
    override_get_db
):
    """
    Test providing list of available muscle groups
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.get(
            f"/api/muscle_groups",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    some_muscle_groups = {"Грудь", "Ноги", "Спина"}
    muscle_groups_from_server = set([item["name"] for item in response.json()])
    assert some_muscle_groups.issubset(muscle_groups_from_server)
