import pytest

from sqlalchemy import select

from src import Exercise
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_all_exercises(create_coach, db):
    """Check list of all exercises"""
    response = await make_test_http_request(f"/api/exercises", "get", create_coach.username)
    assert response.status_code == 200

    available_coach_ids = {create_coach.id, None}
    for exercise in response.json():
        exercise_in_db = await db.execute(
            select(Exercise).where(Exercise.id == exercise["id"])
        )
        # return only user's and default exercises
        assert exercise_in_db.scalar().coach_id in available_coach_ids
