from typing import Protocol


class AbstractNotificator(Protocol):
    """
    Provides interface to any notificator in the application
    """
    def send_notification(self, recipient_id: str, recipient_data: dict):
        """
        Entrypoint to notify user
        """
        raise NotImplementedError("Notificator has to implement send notification method")
