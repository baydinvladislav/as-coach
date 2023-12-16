from typing import Protocol


class AbstractNotificator(Protocol):

    def send_notification(self, recipient_id: str, recipient_data: dict):
        raise NotImplementedError("Notificator has to implement send notification method")
