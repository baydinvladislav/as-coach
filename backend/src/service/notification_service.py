import json
import logging

from src.supplier.firebase_supplier import PushFirebaseNotificator
from src.supplier.kafka_supplier import KafkaSupplier

logger = logging.getLogger(__name__)


class NotificationService:

    def __init__(self, notificator: PushFirebaseNotificator, kafka_supplier: KafkaSupplier):
        self.push_notificator = notificator
        self.kafka_supplier = kafka_supplier

    async def send_push_notification(self, recipient_id: str, recipient_data: dict[str, str]):
        if recipient_id is None:
            logger.warning(f"Failed to send notification recipient id is not specified")
            return

        result = await self.push_notificator.send_notification(recipient_id, recipient_data)
        is_sent = isinstance(result, str) and "ascoach" in result
        if is_sent:
            # TODO: make logging practice like Whoosh
            logger.info(f"Push notifications sent on customer device: {recipient_id}")

    async def send_telegram_customer_invite(self, coach_name: str, customer_username: str, customer_password: str):
        message = json.dumps(
            {"username": customer_username, "customer_password": customer_password, "coach_name": coach_name},
            ensure_ascii=False,
        )
        self.kafka_supplier.send_message(message)
