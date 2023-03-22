from fastapi.testclient import TestClient

from src.main import app


def test_login(db, create_user):
    with TestClient(app) as client:
        response = client.post(
            "/login",
            data={
                "username": create_user.username,
                "password": "my_test_pswd"
            },
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

        assert response.status_code == 200

        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
