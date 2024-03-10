import pytest

from sqlalchemy import select, delete

from src import Customer
from tests.conftest import (
    make_test_http_request
)
from src.config import TEST_CUSTOMER_FIRST_NAME, TEST_CUSTOMER_LAST_NAME, TEST_CUSTOMER_USERNAME


@pytest.mark.asyncio
async def test_create_customer_successfully(create_user, override_get_db, mock_send_kafka_message):
    """
    Successfully customer creation
    """
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": TEST_CUSTOMER_USERNAME
    }

    customer = await override_get_db.execute(
        select(Customer).where(Customer.username == customer_data["phone_number"])
    )

    customer = customer.scalar()
    if customer:
        await override_get_db.execute(
            delete(Customer).where(Customer.username == customer_data["phone_number"])
        )
        await override_get_db.commit()

    response = await make_test_http_request("/api/customers", "post", create_user.username, json=customer_data)
    assert response.status_code == 201

    if response.status_code == 201:
        await override_get_db.execute(
            delete(Customer).where(Customer.username == response.json()["id"])
        )
        await override_get_db.commit()

    mock_send_kafka_message.assert_called_once()


@pytest.mark.asyncio
async def test_create_customer_not_valid_number(create_user, override_get_db):
    """
    Failed because of not valid number
    """
    customer_data = {
        "first_name": "Александр",
        "last_name": "Иванов",
        "phone_number": "+9857773322"
    }

    response = await make_test_http_request("/api/customers", "post", create_user.username, json=customer_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_customer_it_already_exists(create_user, override_get_db):
    """
    Failed because of customer with these last_name + first already exists
    """
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": None
    }

    customer = await override_get_db.execute(
        select(Customer).where(
            Customer.first_name == customer_data["first_name"],
            Customer.last_name == customer_data["last_name"]
        )
    )

    customer = customer.scalar()
    if customer:
        await override_get_db.execute(
            delete(Customer).where(
                Customer.first_name == customer_data["first_name"],
                Customer.last_name == customer_data["last_name"]
            )
        )
        await override_get_db.commit()

    response = await make_test_http_request("/api/customers", "post", create_user.username, json=customer_data)
    assert response.status_code == 201

    # already exists
    response = await make_test_http_request("/api/customers", "post", create_user.username, json=customer_data)
    assert response.status_code == 400

    await override_get_db.execute(
        delete(Customer).where(
            Customer.first_name == TEST_CUSTOMER_FIRST_NAME,
            Customer.last_name == TEST_CUSTOMER_LAST_NAME
        )
    )
    await override_get_db.commit()
