from dataclasses import dataclass, asdict

import firebase_admin
from firebase_admin import initialize_app, messaging, credentials

from src.config import (
    FIREBASE_TYPE,
    FIREBASE_PROJECT_ID,
    FIREBASE_PRIVATE_KEY_ID,
    FIREBASE_PRIVATE_KEY,
    FIREBASE_CLIENT_EMAIL,
    FIREBASE_CLIENT_ID,
    FIREBASE_AUTH_URI,
    FIREBASE_TOKEN_URI,
    FIREBASE_AUTH_PROVIDER_CERT_URL,
    FIREBASE_CLIENT_CERT_URL,
    FIREBASE_UNIVERSE_DOMAIN,
)
from src.application.services.notifications.notificator import AbstractNotificator


class PushNotificationEmptyDataMessage(Exception):
    pass


@dataclass
class FirebaseConfig:
    """
    Download from Firebase web as .json
    """
    type: str = FIREBASE_TYPE
    project_id: str = FIREBASE_PROJECT_ID
    private_key_id: str = FIREBASE_PRIVATE_KEY_ID
    private_key: str = FIREBASE_PRIVATE_KEY
    client_email: str = FIREBASE_CLIENT_EMAIL
    client_id: str = FIREBASE_CLIENT_ID
    auth_uri: str = FIREBASE_AUTH_URI
    token_uri: str = FIREBASE_TOKEN_URI
    auth_provider_x509_cert_url: str = FIREBASE_AUTH_PROVIDER_CERT_URL
    client_x509_cert_url: str = FIREBASE_CLIENT_CERT_URL
    universe_domain: str = FIREBASE_UNIVERSE_DOMAIN


class PushFirebaseNotificator(AbstractNotificator):
    """
    Implements interface to send push notification
    to user device through Firebase platform
    """

    def __init__(self):
        """
        Prepares config to connection
        """
        self.firebase_config = asdict(FirebaseConfig())
        self.firebase_config["private_key"] = self.firebase_config["private_key"].replace('\\n', '\n')

    async def establish_conn_to_firebase(self):
        initialize_app(credentials.Certificate(self.firebase_config))

    async def send_notification(self, recipient_id: str, recipient_data: dict[str, str]) -> str:
        """
        Sends Apple Push Notification instance as payload to send message on user device.
        This method works only with iOS platform to send message on Android platform have to
        pass in message additional parameter look at docs:
        https://firebase.google.com/docs/cloud-messaging/send-message?hl=ru#when-to-use-platform-specific-fields

        Args:
            recipient_id: fcm token to identify user device
            recipient_data: contains message data

        Returns:
            result: string that contains project id and message id as positive response from Firebase
        """
        if not await self._valid_recipient_data(recipient_data):
            raise PushNotificationEmptyDataMessage("Recipient data must have either title and body")

        if not firebase_admin._apps:
            await self.establish_conn_to_firebase()

        aps_data = messaging.Aps(
            alert=messaging.ApsAlert(title=recipient_data["title"], body=recipient_data["body"]),
            sound="default",
        )

        message = messaging.Message(
            token=recipient_id,
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps_data)),
        )

        # TODO: make it async
        result = messaging.send(message)
        return result

    @staticmethod
    async def _valid_recipient_data(recipient_data: dict) -> bool:
        """
        Static until more complex logic
        """
        return "title" in recipient_data and "body" in recipient_data
