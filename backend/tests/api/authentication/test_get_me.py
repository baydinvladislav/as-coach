import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_coach_get_me(create_coach):
    """Tests that coach role can get response from /api/me"""

    response = await make_test_http_request("/api/me", "get", create_coach.username)
    assert response.status_code == 200

    response_json = response.json()

    assert response_json.get("id") is not None
    assert response_json.get("user_type") == "coach"
    assert response_json.get("username") == create_coach.username
    assert response_json.get("first_name") == create_coach.first_name


@pytest.mark.asyncio
async def test_customer_get_me(create_customer):
    """Tests that customer role can get response from /api/me"""

    response = await make_test_http_request("/api/me", "get", create_customer.username)
    assert response.status_code == 200

    response_json = response.json()

    assert response_json.get("id") is not None
    assert response_json["user_type"] == "customer"
    assert response_json.get("username") == create_customer.username
    assert response_json.get("first_name") == create_customer.first_name
