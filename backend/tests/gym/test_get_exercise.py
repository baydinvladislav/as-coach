import pytest

from httpx import AsyncClient

from src.main import app
from src.gym.models import Exercise
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_get_all_exercises(
    create_user,
    create_exercises,
    override_get_db
):
    """
    Check list of all exercises
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.get(
            f"/api/exercises",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    for exercise in response.json():
        exercise_in_db = override_get_db.query(Exercise).get(exercise["id"])
        # return only user's and common exercises
        assert exercise_in_db.coach_id in {create_user.id, None}
