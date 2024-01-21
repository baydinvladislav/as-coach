import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_customer_login_successfully(create_customer):
    """
    Tests success customer login
    """
    login_data = {
        "username": create_customer.username,
        "password": create_customer.password,
        "fcm_token": "test token value",
    }

    response = await make_test_http_request("/api/login", "post", create_customer.username, data=login_data)
    assert response.status_code == 200
