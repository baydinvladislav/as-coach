from datetime import date, timedelta
import pytest

from httpx import AsyncClient
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.main import app
from src.customer.models import TrainingPlan
from src.gym.models import MuscleGroup, ExercisesOnTraining
from src.auth.utils import create_access_token


@pytest.mark.asyncio
async def test_create_training_plan_successfully(
        create_customer,
        create_exercises,
        override_get_db
):
    """
    Successfully training plan creation
    """
    muscle_groups = await override_get_db.execute(
        select(MuscleGroup).options(selectinload(MuscleGroup.exercises))
    )

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
    for muscle in muscle_groups.scalars():
        trainings.append({
            "name": muscle.name,
            "exercises": [dict(id=str(exercise.id), sets=[12, 12, 12], supersets=[]) for exercise in muscle.exercises]
        })

    training_plan_data["trainings"] = trainings

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_customer.coach.username)
        response = await ac.post(
            f"/api/customers/{create_customer.id}/training_plans",
            json=training_plan_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201

    if response.status_code == 201:
        await override_get_db.execute(
            delete(TrainingPlan).where(TrainingPlan.id == response.json()["id"])
        )
        await override_get_db.commit()


@pytest.mark.asyncio
async def test_create_training_plan_with_supersets_successfully(
        create_customer,
        create_exercises,
        override_get_db
):
    """
    Successfully creating training plan with supersets
    """
    muscle_groups = await override_get_db.execute(
        select(MuscleGroup).options(selectinload(MuscleGroup.exercises))
    )

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
    for muscle in muscle_groups.scalars():
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
        auth_token = await create_access_token(create_customer.coach.username)
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
    exercises_in_superset = await override_get_db.execute(
        select(ExercisesOnTraining).where(
            ExercisesOnTraining.exercise_id.in_(superset_exercises_ids)
        )
    )

    s = set()
    for e in exercises_in_superset.scalars():
        s.add(e.superset_id)

    assert len(s) == 1
    s.clear()

    triset_exercises_ids = (
        first_exercise_id_in_triset,
        second_exercise_id_in_triset,
        third_exercise_id_in_triset
    )
    exercises_in_triset = await override_get_db.execute(
        select(ExercisesOnTraining).where(
            ExercisesOnTraining.exercise_id.in_(triset_exercises_ids)
        )
    )

    for e in exercises_in_triset.scalars():
        s.add(e.superset_id)

    assert len(s) == 1

    if response.status_code == 201:
        await override_get_db.execute(
            delete(TrainingPlan).where(TrainingPlan.id == response.json()["id"])
        )
        await override_get_db.commit()


@pytest.mark.asyncio
async def test_get_training_plan_with_supersets(
    create_customer,
    create_training_plans,
    create_training_exercises,
    override_get_db
):

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_customer.coach.username)
        response = await ac.get(
            f"/api/customers/{create_customer.id}/training_plans/{create_training_plans[0].id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    chest_training = list(filter(lambda x: x["name"] == "Грудь", response.json()["trainings"]))[0]
    superset_ids_set = set()
    for exercise in chest_training["exercises"]:
        superset_ids_set.add(exercise["superset_id"])

    assert len(superset_ids_set) == 1

    if response.status_code == 200:
        await override_get_db.execute(
            delete(TrainingPlan).where(TrainingPlan.id == str(create_training_plans[0].id))
        )
        await override_get_db.commit()
