from datetime import date, timedelta
import pytest

from httpx import AsyncClient

from src.main import app
from src.customer.models import TrainingPlan
from src.gym.models import MuscleGroup, ExercisesOnTraining
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
            "exercises": [dict(id=str(exercise.id), sets=[12, 12, 12], supersets=[]) for exercise in muscle.exercises]
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


@pytest.mark.anyio
async def test_create_training_plan_with_supersets_successfully(
        create_customer,
        create_exercises,
        override_get_db
):
    """
    Successfully creating training plan with supersets
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
            "exercises": [dict(id=str(exercise.id), sets=[12, 12, 12], supersets=[]) for exercise in muscle.exercises],
        })

    training_plan_data["trainings"] = trainings

    # link exercises to supersets:

    # first superset
    first_exercise_id_in_superset = training_plan_data["trainings"][0]["exercises"][0]["id"]
    second_exercise_id_in_superset = training_plan_data["trainings"][0]["exercises"][1]["id"]

    training_plan_data["trainings"][0]["exercises"][0]["supersets"].append(second_exercise_id_in_superset)
    training_plan_data["trainings"][0]["exercises"][1]["supersets"].append(first_exercise_id_in_superset)

    # second superset is tri-set
    first_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][0]["id"]
    second_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][1]["id"]
    third_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][2]["id"]

    training_plan_data["trainings"][1]["exercises"][0]["supersets"].append(second_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][0]["supersets"].append(third_exercise_id_in_triset)

    training_plan_data["trainings"][1]["exercises"][1]["supersets"].append(first_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][1]["supersets"].append(third_exercise_id_in_triset)

    training_plan_data["trainings"][1]["exercises"][2]["supersets"].append(first_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][2]["supersets"].append(second_exercise_id_in_triset)

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

    superset_exercises_ids = (
        first_exercise_id_in_superset,
        second_exercise_id_in_superset
    )
    exercises_in_superset = override_get_db.query(ExercisesOnTraining).filter(
        ExercisesOnTraining.exercise_id.in_(superset_exercises_ids)
    ).all()

    s = set()
    for e in exercises_in_superset:
        s.add(e.superset_id)

    assert len(s) == 1
    s.clear()

    triset_exercises_ids = (
        first_exercise_id_in_triset,
        second_exercise_id_in_triset,
        third_exercise_id_in_triset
    )
    exercises_in_triset = override_get_db.query(ExercisesOnTraining).filter(
        ExercisesOnTraining.exercise_id.in_(triset_exercises_ids)
    ).all()

    for e in exercises_in_triset:
        s.add(e.superset_id)

    assert len(s) == 1

    if response.status_code == 201:
        training_plan = override_get_db.query(TrainingPlan).filter(
            TrainingPlan.id == response.json()["id"]
        ).first()
        override_get_db.delete(training_plan)
        override_get_db.commit()
