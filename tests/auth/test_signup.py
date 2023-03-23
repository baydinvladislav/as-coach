from fastapi.testclient import TestClient
from fastapi import status

from src.main import app
from tests.conftest import TEST_SIGNUP_USER_LOGIN, TEST_USER_PASSWORD


def test_signup_new_user():
    with TestClient(app) as client:
        body = {
            "username": TEST_SIGNUP_USER_LOGIN,
            "password": TEST_USER_PASSWORD
        }

        response = client.post("/signup", json=body)
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED

        assert "id" in response.json()
        assert response.json()["username"] == body["username"]
