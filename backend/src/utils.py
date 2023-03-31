def validate_phone_number(phone_number: str):
    """
    We have to get: +79xxxxxxxxx
    Phone number must contain 12 numbers
    """
    if phone_number.startswith("+7") and len(phone_number) == 12:
        return phone_number
    raise ValueError("Specify correct phone number")
