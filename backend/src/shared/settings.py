import os


class TelegramSettings:
    api_id: int = os.environ.get("API_ID", int())
    api_hash: str = os.environ.get("API_HASH", str())
