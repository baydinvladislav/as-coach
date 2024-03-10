import pytest
from unittest.mock import patch


@pytest.fixture
def mock_send_kafka_message():
    with patch("src.supplier.kafka.KafkaSupplier.send_message") as mock:
        yield mock


@pytest.fixture
def mock_send_notification():
    with patch("src.service.notifications.notification_service.NotificationService.send_notification") as mock:
        yield mock
