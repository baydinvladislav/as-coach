from datetime import timedelta
import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_training_plans):
    customer_username = create_training_plans[0].customer.username
    specific_day = create_training_plans[0].start_date + timedelta(days=3)

    response = await make_test_http_request(
        url=f"api/nutrition/diets/{specific_day}",
        method="get",
        username=customer_username,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_product(create_customer):
    response = await make_test_http_request(
        url="api/nutrition/products/lookup?query_text=молоко",
        method="get",
        username=create_customer.username,
    )
    assert response.status_code == 200
