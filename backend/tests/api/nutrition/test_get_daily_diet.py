import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_customer):
    response = await make_test_http_request(
        url="api/nutrition/products/lookup?query_text=молоко",
        method="get",
        username=create_customer.username,
    )
    assert response.status_code == 200
