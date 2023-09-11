import pytest

from httpx import AsyncClient
from sqlalchemy import select

from src.main import app
from src import Exercise
from src.utils import create_access_token


@pytest.mark.asyncio
async def test_get_all_exercises(
    create_user,
    create_exercises,
    override_get_db
):
    """
    Check list of all exercises
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.get(
            f"/api/exercises",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    available_coach_ids = {create_user.id, None}
    for exercise in response.json():
        exercise_in_db = await override_get_db.execute(
            select(Exercise).where(
                Exercise.id == exercise["id"]
            )
        )
        # return only user's and common exercises
        assert exercise_in_db.scalar().coach_id in available_coach_ids
