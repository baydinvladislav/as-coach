import pytest

from httpx import AsyncClient
from sqlalchemy import select, delete

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
    muscle_groups = await override_get_db.execute(select(MuscleGroup))
    muscle_groups = muscle_groups.scalars().first()
    exercise_data = {
        "name": "My custom exercise",
        "muscle_group_id": str(muscle_groups.id)
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.post(
            f"/api/exercises",
            json=exercise_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201

    if response.status_code == 201:
        await override_get_db.execute(
            delete(Exercise).where(
                Exercise.id == response.json()["id"]
            )
        )
        await override_get_db.commit()
