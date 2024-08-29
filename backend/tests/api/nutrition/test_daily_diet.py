from datetime import timedelta
import pytest
import uuid

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_diets):
    customer_username = create_diets[0].training_plans.customer.username
    specific_day = create_diets[0].training_plans.start_date + timedelta(days=2)

    response = await make_test_http_request(
        url=f"api/nutrition/diets/{specific_day}",
        method="get",
        username=customer_username,
    )

    assert response.status_code == 200

    response = response.json()
    assert "date" in response
    assert "actual_nutrition" in response

    meals = response["actual_nutrition"]
    assert "daily_total" in meals
    assert "breakfast" in meals
    assert "lunch" in meals
    assert "dinner" in meals
    assert "snacks" in meals


@pytest.mark.asyncio
async def test_add_product_to_diet(create_diets):
    diet_id = str(create_diets[0].id)
    customer_username = create_diets[0].training_plans.customer.username

    product_data = {
        "diet_id": diet_id,
        "product_data": [
            {"id": "406c4cec-a14f-4424-8507-3df2a7954fdd", "amount": 180},
            {"id": "0422799b-69ab-464f-8535-ef11ee575863", "amount": 220},
        ],
        "meal_type": "breakfast",
        "specific_day": str(create_diets[0].training_plans.start_date + timedelta(days=2)),
    }

    response = await make_test_http_request(
        url=f"api/nutrition/diets",
        method="post",
        json=product_data,
        username=customer_username,
    )

    assert response.status_code == 201
