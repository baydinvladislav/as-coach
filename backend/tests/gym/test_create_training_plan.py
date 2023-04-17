from datetime import date, timedelta
import pytest

from httpx import AsyncClient

from src.main import app
from src.customer.models import TrainingPlan
from src.gym.models import MuscleGroup
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_create_training_plan_successfully(
        create_customer,
        create_exercises,
        override_get_db
):
    """
    Successfully training plan creation
    """
    muscle_groups = override_get_db.query(MuscleGroup).all()

    training_plan_data = {
        "start_date": date.today().strftime('%Y-%m-%d'),
        "end_date": (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "diets": [
            {
                "proteins": 200,
                "fats": 100,
                "carbs": 400
            }
        ],
        "set_rest": 60,
        "exercise_rest": 120
    }

    trainings = []
    for muscle in muscle_groups:
        trainings.append({
            "name": muscle.name,
            "exercises": [dict(id=str(exercise.id), sets=[12, 12, 12]) for exercise in muscle.exercises]
        })

    training_plan_data["trainings"] = trainings

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.user.username)
        response = await ac.post(
            f"/api/customers/{create_customer.id}/training_plans",
            json=training_plan_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201

    if response.status_code == 201:
        training_plan = override_get_db.query(TrainingPlan).filter(
            TrainingPlan.id == response.json()["id"]
        ).first()
        override_get_db.delete(training_plan)
        override_get_db.commit()
