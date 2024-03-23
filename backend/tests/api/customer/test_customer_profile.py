import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_customer_get_profile(create_customer, db):
    """
    Tests that customer can get profile on /api/profiles
    """
    response = await make_test_http_request("/api/profiles", "get", create_customer.username)
    assert response.status_code == 200
    assert response.json()["user_type"] == "customer"


@pytest.mark.asyncio
async def test_customer_update_profile(create_customer, db):
    """
    Tests that customer can update profile on /api/profiles
    """
    updated_data = {
        "username": create_customer.username,
        "first_name": create_customer.first_name,
        "email": "newemail@gmail.com",
        "last_name": "Petrov"
    }

    response = await make_test_http_request("/api/profiles", "post", create_customer.username, data=updated_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["email"] == updated_data["email"]
    assert response_data["last_name"] == updated_data["last_name"]
    assert response_data["user_type"] == "customer"
