"""
Common utils for project
"""

import uuid


def validate_phone_number(phone_number: str):
    """
    We have to get: +79xxxxxxxxx
    Phone number must contain 12 numbers
    """
    if phone_number.startswith("+7") and len(phone_number) == 12:
        return phone_number
    raise ValueError("Specify correct phone number")


async def validate_uuid(uuid_value: str):
    """
    Validates passed uuid
    """
    try:
        uuid.UUID(str(uuid_value))
        return True
    except ValueError:
        return False
