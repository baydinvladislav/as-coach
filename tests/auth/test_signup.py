from fastapi.testclient import TestClient

from src.main import app


def test_signup_new_user():
    with TestClient(app) as client:
        body = {
            "username": "+79857914688",
            "password": "my_test_pswd"
        }

        response = client.post("/signup", json=body)
        assert response.status_code == 201

        assert "id" in response.json()
        assert response.json()["username"] == body["username"]
