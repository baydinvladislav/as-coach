import pytest
from unittest.mock import patch


@pytest.fixture
def mock_send_kafka_message():
    with patch("src.supplier.kafka_supplier.KafkaSupplier.send_message") as mock:
        yield mock


@pytest.fixture
def mock_send_push_notification():
    with patch("src.service.notification_service.NotificationService.send_push_notification") as mock:
        yield mock
