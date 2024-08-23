from datetime import timedelta
import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_diets):
    customer_username = create_diets[0].training_plans.customer.username
    specific_day = create_diets[0].training_plans.start_date + timedelta(days=3)

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
async def test_get_product(create_customer):
    response = await make_test_http_request(
        url="api/nutrition/products/lookup?query_text=молоко",
        method="get",
        username=create_customer.username,
    )
    assert response.status_code == 200
