from telethon import TelegramClient

from src.shared.settings import TelegramSettings


class TelegramAdapter:
    settings: TelegramSettings = TelegramSettings()
    client: TelegramClient | None = None

    async def __aenter__(self):
        await self.establish_connect()
        return self

    async def close_connect(self):
        self.client.disconnect()

    async def send_message_to_user(self, username: str, message: str) -> None:
        await self.client.send_message(username, message)

    async def establish_connect(self):
        if self.client is None:
            self.client = TelegramClient('session_name', self.settings.api_id, api_hash=self.settings.api_hash)
            self.client.start()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close_connect()
