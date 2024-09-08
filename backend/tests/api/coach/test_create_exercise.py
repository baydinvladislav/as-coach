import pytest

from sqlalchemy import select

from src import MuscleGroup
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_create_exercise_successfully(create_coach, create_customer, create_exercises, db):
    """Successfully exercise creation"""
    muscle_groups = await db.execute(select(MuscleGroup))
    muscle_groups = muscle_groups.scalars().first()
    exercise_data = {
        "name": "My custom exercise",
        "muscle_group_id": str(muscle_groups.id)
    }

    response = await make_test_http_request(f"/api/exercises", "post", create_coach.username, json=exercise_data)
    assert response.status_code == 201

    response_json = response.json()

    assert response_json.get("id") is not None
    assert response_json.get("name") == exercise_data.get("name")
