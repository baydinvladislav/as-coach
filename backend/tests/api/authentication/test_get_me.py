import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_coach_get_me(create_user, override_get_db):
    """
    Tests that coach can get response from /api/me
    """
    response = await make_test_http_request("/api/me", "get", create_user.username)

    assert response.status_code == 200
    assert response.json()["user_type"] == "coach"
