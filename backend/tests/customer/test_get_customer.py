import pytest
from httpx import AsyncClient

from src.main import app
from src.customer.models import Customer
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_get_customers(create_user, override_get_db):
    """
    Gets all user's customers
    """
    customers_data = [
        {
            "first_name": "Александр",
            "last_name": "Петров",
            "phone_number": "+79850002233"
        },
        {
            "first_name": "Дарья",
            "last_name": "Сахарова",
            "phone_number": "+79097773322"
        },
        {
            "first_name": "Андрей",
            "last_name": "Астафьев",
            "phone_number": "+79267334422"
        }
    ]

    ids = []
    for customer in customers_data:
        async with AsyncClient(app=app, base_url="http://as-coach") as ac:
            auth_token = create_access_token(create_user.username)
            response = await ac.post(
                "/api/customers",
                json=customer,
                headers={
                    "Authorization": f"Bearer {auth_token}"
                }
            )

        assert response.status_code == 201
        ids.append(response.json()["id"])

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.get(
            "/api/customers",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    override_get_db.query(Customer).filter(Customer.id.in_(ids)).delete()
    override_get_db.commit()


@pytest.mark.anyio
async def test_get_specific_customer(create_user, override_get_db):
    """
    Gets specific customer
    """
    customer_data = {
        "first_name": "Александр",
        "last_name": "Петров",
        "phone_number": "+79850002233"
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.post(
            "/api/customers",
            json=customer_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201
    customer_id = response.json()["id"]

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.get(
            f"/api/customers/{customer_id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200
    assert response.json()["id"] == customer_id

    override_get_db.query(Customer).filter(Customer.id == customer_id).delete()
    override_get_db.commit()


@pytest.mark.anyio
async def test_get_specific_customer_failed_not_valid_uuid(create_user, override_get_db):
    """
    Failed because client sent is not valid UUID
    """
    customer_data = {
        "first_name": "Александр",
        "last_name": "Петров",
        "phone_number": "+79850002233"
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.post(
            "/api/customers",
            json=customer_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201
    customer_id = response.json()["id"]

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.get(
            f"/api/customers/{customer_id[:-1]}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 400

    override_get_db.query(Customer).filter(Customer.id == customer_id).delete()
    override_get_db.commit()
