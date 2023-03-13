from fastapi.testclient import TestClient

from src.main import app


def test_signup_new_user():
    with TestClient(app) as client:
        json = {
            "username": "79857994488",
            "password": "my_pswd"
        }

        response = client.post("/signup", json=json)
        assert response.status_code == 201
