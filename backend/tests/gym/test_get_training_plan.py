import pytest

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
    Check that user can get all customer's training plans
    """
    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.user.username)
        response = await ac.get(
            f"/api/customers/{create_customer.id}/training_plans/",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()[0]["end_date"] > response.json()[-1]["end_date"]
