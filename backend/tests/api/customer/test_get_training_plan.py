import pytest
from datetime import datetime

from sqlalchemy import delete

from src import TrainingPlan
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_all_training_plans(
    create_customer,
    create_exercises,
    create_diets,
    create_training_plans,
    db,
):
    """
    Checks that user can get all customer's training plans
    Checks training plans order
    """
    response = await make_test_http_request(
        f"/api/customers/{create_customer.id}/training_plans", "get", create_customer.coach.username
    )
    assert response.status_code == 200

    response_data = response.json()
    assert len(create_training_plans) == len(response_data)

    # check descending dates
    first_date_end = datetime.strptime(response_data[0]["end_date"], "%Y-%m-%d").date()
    last_date_end = datetime.strptime(response_data[-1]["end_date"], "%Y-%m-%d").date()
    assert first_date_end > last_date_end


@pytest.mark.asyncio
async def test_get_specified_training_plan(
    create_customer,
    create_training_exercises,
    create_trainings,
    create_diets,
    db,
):
    """
    Returns specified training plan
    """
    training_plan_id = str(create_trainings[0].training_plan_id)
    response = await make_test_http_request(
        url=f"/api/customers/{create_customer.id}/training_plans/{training_plan_id}",
        method="get",
        username=create_customer.coach.username
    )
    assert response.status_code == 200
    response_json = response.json()

    # we have existed training plan
    assert response.json()["id"] == training_plan_id

    # check that we have correct exercise ordering
    first_exercise = response_json["trainings"][0]["exercises"][0]
    second_exercise = response_json["trainings"][0]["exercises"][1]
    # assert first_exercise["ordering"] < second_exercise["ordering"]


@pytest.mark.asyncio
async def test_get_training_plan_with_supersets(
    create_customer,
    create_training_plans,
    create_diets,
    create_training_exercises,
    db,
):
    response = await make_test_http_request(
        url=f"/api/customers/{create_customer.id}/training_plans/{create_training_plans[0].id}",
        method="get",
        username=create_customer.coach.username,
    )
    assert response.status_code == 200

    chest_training = list(filter(lambda x: x["name"] == "Грудь", response.json()["trainings"]))[0]
    superset_ids_set = set()
    for exercise in chest_training["exercises"]:
        superset_ids_set.add(exercise["superset_id"])

    # exercises have the same superset_id
    assert len(superset_ids_set) == 1

    if response.status_code == 200:
        await db.execute(
            delete(TrainingPlan).where(TrainingPlan.id == str(create_training_plans[0].id))
        )
        await db.commit()
