from typing import Protocol


class AbstractNotificator(Protocol):
    """
    Provides interface to any notificator in the application
    """
    async def send_notification(self, recipient_id: str, recipient_data: dict[str, str]):
        """
        Entrypoint to notify user
        """
        raise NotImplementedError("Notificator has to implement send notification method")
