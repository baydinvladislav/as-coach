import pytest
from datetime import datetime

from httpx import AsyncClient

from src.main import app
from src.auth.utils import create_access_token


@pytest.mark.anyio
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
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.user.username)
        response = await ac.get(
            f"/api/customers/{create_customer.id}/training_plans",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    first_date_end = datetime.strptime(response.json()[0]["end_date"], '%Y-%m-%d').date()
    last_date_end = datetime.strptime(response.json()[-1]["end_date"], '%Y-%m-%d').date()
    assert first_date_end > last_date_end


@pytest.mark.anyio
async def test_get_specified_training_plan(
        create_customer,
        create_exercises,
        create_training_plans,
        override_get_db
):
    """
    Returns specified training plan
    """
    training_plan = create_training_plans[0]

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.user.username)
        response = await ac.get(
            f"/api/customers/{create_customer.id}/training_plans/{training_plan.id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["id"] == str(training_plan.id)
