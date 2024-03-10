import pytest

from sqlalchemy import delete

from src import Customer
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customers(create_user, override_get_db, mock_send_kafka_message):
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
        response = await make_test_http_request("/api/customers", "post", user_username, json=customer)
        assert response.status_code == 201
        ids.append(response.json()["id"])

    response = await make_test_http_request("/api/customers", "get", user_username)
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
    response = await make_test_http_request(
        f"/api/customers/{create_customer.id}", "get", create_customer.coach.username
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
    response = await make_test_http_request(f"/api/customers/7a8sdgajksd8asdb", "get", create_user.username)
    assert response.status_code == 400
