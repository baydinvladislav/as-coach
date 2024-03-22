import pytest

from src.shared.config import TEST_CUSTOMER_FIRST_NAME, TEST_CUSTOMER_LAST_NAME
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_create_customer_successfully_with_telegram_username(create_coach, mock_send_kafka_message):
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": "@test_telegram_user",
    }

    response = await make_test_http_request("/api/customers", "post", create_coach.username, json=customer_data)
    assert response.status_code == 201

    # check that we sent customer invite in application through Telegram using Kafka
    mock_send_kafka_message.assert_called_once()


@pytest.mark.asyncio
async def test_create_customer_successfully_without_telegram_username(create_coach, mock_send_kafka_message):
    customer_data = {
        "first_name": TEST_CUSTOMER_FIRST_NAME,
        "last_name": TEST_CUSTOMER_LAST_NAME,
        "phone_number": None,
    }

    response = await make_test_http_request("/api/customers", "post", create_coach.username, json=customer_data)
    assert response.status_code == 201

    # check that we didn't send customer invite in application through Telegram using Kafka
    mock_send_kafka_message.assert_not_called()


@pytest.mark.asyncio
async def test_create_customer_it_already_exists(create_customer):
    customer_data = {
        "first_name": create_customer.first_name,
        "last_name": create_customer.last_name,
        "phone_number": None
    }

    response = await make_test_http_request(
        "/api/customers", "post", create_customer.coach.username, json=customer_data
    )
    assert response.status_code == 400
