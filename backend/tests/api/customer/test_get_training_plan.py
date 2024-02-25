import pytest
from datetime import datetime

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_all_training_plans(
        create_customer,
        create_exercises,
        create_training_plans,
        override_get_db
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
        override_get_db
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
    assert response.json()["id"] == training_plan_id
