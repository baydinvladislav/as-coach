from fastapi.testclient import TestClient
from fastapi import status

from src.main import app
from tests.conftest import TEST_USER_PASSWORD


def test_login(create_user):
    with TestClient(app) as client:
        response = client.post(
            "/login",
            data={
                "username": create_user.username,
                "password": TEST_USER_PASSWORD
            },
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        assert response.status_code == status.HTTP_200_OK

        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
