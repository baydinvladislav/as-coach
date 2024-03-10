import pytest
from unittest.mock import patch


@pytest.fixture
def mock_send_kafka_message():
    with patch("src.supplier.notifications.kafka.KafkaSupplier.send_message") as mock:
        yield mock
