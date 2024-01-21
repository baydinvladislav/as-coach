import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_customer_get_me(create_customer, override_get_db):
    """
    Tests that customer can get response from /api/me
    """
    response = await make_test_http_request("/api/me", "get", create_customer.username)
    assert response.status_code == 200
    assert response.json()["user_type"] == "customer"
