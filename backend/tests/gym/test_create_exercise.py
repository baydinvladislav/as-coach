import pytest

from httpx import AsyncClient

from src.main import app
from src.gym.models import MuscleGroup, Exercise
from src.auth.utils import create_access_token


@pytest.mark.asyncio
async def test_create_exercise_successfully(
    create_user,
    create_customer,
    create_exercises,
    override_get_db
):
    """
    Successfully exercise creation
    """
    muscle_groups = override_get_db.query(MuscleGroup).all()

    exercise_data = {
        "name": "My custom exercise",
        "muscle_group_id": str(muscle_groups[0].id)
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.post(
            f"/api/exercises",
            json=exercise_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201

    if response.status_code == 201:
        exercise = override_get_db.query(Exercise).filter(
            Exercise.id == response.json()["id"]
        ).first()
        override_get_db.delete(exercise)
        override_get_db.commit()
