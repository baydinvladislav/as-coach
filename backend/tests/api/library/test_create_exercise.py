import pytest

from sqlalchemy import select, delete

from src import MuscleGroup, Exercise
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_create_exercise_successfully(
    create_coach,
    create_customer,
    create_exercises,
    override_get_db
):
    """
    Successfully exercise creation
    """
    muscle_groups = await override_get_db.execute(select(MuscleGroup))
    muscle_groups = muscle_groups.scalars().first()
    exercise_data = {
        "name": "My custom exercise",
        "muscle_group_id": str(muscle_groups.id)
    }

    response = await make_test_http_request(f"/api/exercises", "post", create_coach.username, json=exercise_data)
    assert response.status_code == 201

    if response.status_code == 201:
        await override_get_db.execute(
            delete(Exercise).where(Exercise.id == response.json()["id"])
        )
        await override_get_db.commit()
