import os
import logging
from dataclasses import dataclass

from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class KafkaSettings:
    topic: str = "new.topic.name"
    bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


class KafkaSupplier:

    def __init__(self, config, topic):
        self.producer = Producer(**config)
        self.topic = topic
        logger.info(f"Kafka init")

    def acked(self, err, msg):
        if err is not None:
            logger.warning(f"Failed to deliver message: {msg.value()}: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_message(self, message):
        logger.info(f"Send in {self.topic=} topic {message}")
        self.producer.produce(self.topic, message.encode('utf-8'), callback=self.acked)
        self.producer.poll(0)

    def close(self):
        self.producer.flush()


kafka_settings = KafkaSettings()
