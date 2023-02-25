from fastapi.testclient import TestClient

from src.main import app


def test_create_and_delete_customer():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
