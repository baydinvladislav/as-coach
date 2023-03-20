"""
Schemas for auth service
"""

from pydantic import BaseModel, validator


class UserRegisterIn(BaseModel):
    """
    Schema for user registration
    """
    username: str
    password: str

    @validator("username")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        """
        We have to get: +79xxxxxxxxx
        Phone number contains 9 numbers
        """
        if value.startswith("+7") and len(value) == 12:
            return value
        raise ValueError("Specify correct phone number")

    @validator("password")
    def validate_password(cls, value):  # pylint: disable=no-self-argument
        """
        Simple password
        """
        if 8 <= len(value) <= 128:
            return value
        raise ValueError("Password must be greater than 7 symbols and less than 129 symbols")


class UserRegisterOut(BaseModel):
    """
    Response after success user registration
    """
    id: str
    username: str


class TokenSchema(BaseModel):
    """
    Validates token schema
    """
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """
    Validates token payload
    """
    sub: str
    exp: int
