import logging
from src.application.services.notifications.notificator import AbstractNotificator

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Entrypoint to push notification functionality.
    Uses notificator instance to notify clients
    """
    def __init__(self, notificator: AbstractNotificator):
        self.push_notificator = notificator

    def send_notification(self, recipient_id: str, recipient_data: dict[str, str]):
        if recipient_id is None:
            logger.warning(f"Failed to send notification recipient id is not specified")
            return

        result = self.push_notificator.send_notification(recipient_id, recipient_data)
        is_sent = isinstance(result, str) and "ascoach" in result
        if is_sent:
            # TODO: make logging practice like Whoosh
            logger.info(f"Push notifications sent on customer device: {recipient_id}")
