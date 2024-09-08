import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_all_muscle_groups(create_coach, create_exercises, db):
    """Test providing list of available muscle groups"""

    response = await make_test_http_request(f"/api/muscle_groups", "get", create_coach.username)
    assert response.status_code == 200

    some_muscle_groups = {"Грудь", "Ноги", "Спина"}

    response_json = response.json()

    muscle_groups_from_server = set([item["name"] for item in response_json])
    assert some_muscle_groups.issubset(muscle_groups_from_server)

    for item in response_json:
        assert item.get("id") is not None
        assert item.get("name") is not None
