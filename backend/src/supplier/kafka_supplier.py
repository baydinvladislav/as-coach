import os
import logging
from dataclasses import dataclass

from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class KafkaSettings:
    customer_invite_topic: str = os.getenv("KAFKA_CUSTOMER_INVITE_TOPIC", "")
    bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")


class KafkaSupplier:

    def __init__(self, config, topic):
        self.producer = Producer(**config)
        self.topic = topic

    def acked(self, err, msg):
        if err is not None:
            logger.warning(f"Failed to deliver message: {msg.value()}: {err}")
        else:
            logger.info(f"Message successfully sent in {msg.customer_invite_topic()} [{msg.partition()}]")

    def send_message(self, message):
        self.producer.produce(self.topic, message.encode('utf-8'), callback=self.acked)
        self.producer.poll(0)
        logger.info(f"Message successfully sent in {self.topic}: {message}")

    def close(self):
        self.producer.flush()


kafka_settings = KafkaSettings()
