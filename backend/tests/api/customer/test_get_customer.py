import pytest

from httpx import AsyncClient
from sqlalchemy import delete

from src.main import app
from src import Customer
from src.utils import create_access_token


@pytest.mark.asyncio
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
    user_username = create_user.username

    ids = []
    for customer in customers_data:
        async with AsyncClient(app=app, base_url="http://as-coach") as ac:
            auth_token = await create_access_token(user_username)
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
        auth_token = await create_access_token(user_username)
        response = await ac.get(
            "/api/customers",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    await override_get_db.execute(
        delete(Customer).where(Customer.id.in_(ids))
    )
    await override_get_db.commit()


@pytest.mark.asyncio
async def test_get_specific_customer(create_customer, override_get_db):
    """
    Gets specific customer
    """

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_customer.coach.username)
        response = await ac.get(
            f"/api/customers/{create_customer.id}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    await override_get_db.execute(
        delete(Customer).where(Customer.id == str(create_customer.id))
    )
    await override_get_db.commit()


@pytest.mark.asyncio
async def test_get_specific_customer_failed_not_valid_uuid(create_user, override_get_db):
    """
    Failed because client sent is not valid UUID
    """

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_user.username)
        response = await ac.get(
            f"/api/customers/7a8sdgajksd8asdb",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_ordering_in_get_customers(create_customer, override_get_db):
    """
    Checks that ordering matches the logic in ASC-0083
    """

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = await create_access_token(create_customer.coach.username)
        response = await ac.get(
            f"/api/customers",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 200

    print(f"PYTHON LOGS FROM {response.json()}")
