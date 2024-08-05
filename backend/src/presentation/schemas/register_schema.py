from pydantic import BaseModel, validator

from src.utils import validate_phone_number, validate_password


class UserRegistrationData(BaseModel):
    first_name: str
    password: str


class CoachRegistrationData(UserRegistrationData):
    username: str
    fcm_token: str

    @validator("username")
    def validate_phone_number(cls, value: str):
        return validate_phone_number(value)

    @validator("password")
    def validate_password(cls, value: str):
        return validate_password(value)


class CustomerRegistrationData(UserRegistrationData):
    coach_id: str
    coach_name: str
    password: str
    telegram_username: str | None
    last_name: str


class UserRegisterOut(BaseModel):
    """
    Response after success coach registration
    """
    id: str
    username: str
    first_name: str
    access_token: str
    refresh_token: str
