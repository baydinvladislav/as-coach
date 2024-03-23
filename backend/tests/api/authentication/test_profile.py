import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_user_profile(create_coach):
    """
    Success getting user profile
    """
    response = await make_test_http_request("/api/profiles", "get", create_coach.username)

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == create_coach.username
    assert response.json()["first_name"] == create_coach.first_name
    assert response.json()["user_type"] == "coach"


@pytest.mark.asyncio
async def test_update_user_profile(create_coach):
    """
    Success updating user profile
    """
    prev_last_name = create_coach.last_name

    update_user_data = {
        "first_name": create_coach.first_name,
        "username": create_coach.username,
        "last_name": prev_last_name[::-1],
        "email": "example@yandex.ru"
    }

    response = await make_test_http_request("/api/profiles", "post", create_coach.username, data=update_user_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["last_name"] != prev_last_name
    assert response_data["last_name"] == update_user_data["last_name"]
    assert response_data["email"] == update_user_data["email"]
    assert response_data["user_type"] == "coach"
