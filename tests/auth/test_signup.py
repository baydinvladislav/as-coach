from fastapi.testclient import TestClient

from src.auth.utils import get_hashed_password
from src.main import app


def test_signup_new_user():
    with TestClient(app) as client:
        body = {
            "username": "79857994488",
            "password": get_hashed_password("my_pswd")
        }

        response = client.post("/signup", json=body)
        assert response.status_code == 201

        assert "id" in response.json()
        assert response.json()["username"] == body["username"]
