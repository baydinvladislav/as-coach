import pytest
from httpx import AsyncClient

from src.main import app
from src.customer.models import Customer
from src.auth.utils import create_access_token
from tests.conftest import (
    TEST_CUSTOMER_FIRST_NAME, TEST_CUSTOMER_LAST_NAME, TEST_CUSTOMER_USERNAME
)


@pytest.mark.anyio
async def test_create_customer_successfully(create_user, override_get_db):
    """
    Successfully customer creation
    """
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": TEST_CUSTOMER_USERNAME
    }

    customer = override_get_db.query(Customer).filter(
        Customer.username == customer_data["phone_number"]
    ).first()
    if customer:
        override_get_db.delete(customer)
        override_get_db.commit()

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

    if response.status_code == 201:
        customer = override_get_db.query(Customer).filter(
            Customer.id == response.json()["id"]
        ).first()
        override_get_db.delete(customer)
        override_get_db.commit()


@pytest.mark.anyio
async def test_create_customer_not_valid_number(create_user, override_get_db):
    """
    Failed because of not valid number
    """
    customer_data = {
        "first_name": "Александр",
        "last_name": "Иванов",
        "phone_number": "+9857773322"
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

    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_customer_it_already_exists(create_user, override_get_db):
    """
    Failed because of customer with these last_name + first already exists
    """
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": None
    }

    customer = override_get_db.query(Customer).filter(
        Customer.first_name == customer_data["first_name"],
        Customer.last_name == customer_data["last_name"],
    ).first()
    if customer:
        override_get_db.delete(customer)
        override_get_db.commit()

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

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_user.username)
        response = await ac.post(
            "/api/customers",
            json=customer_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 400

    override_get_db.query(Customer).filter(
        Customer.first_name == response.json()["first_name"],
        Customer.last_name == response.json()["last_name"],
    ).first()

    override_get_db.delete(customer)
    override_get_db.commit()
