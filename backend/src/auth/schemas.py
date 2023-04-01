"""
Schemas for auth service
"""

from pydantic import BaseModel, validator

from src.utils import validate_phone_number


class UserRegisterIn(BaseModel):
    """
    Schema for user registration
    """
    username: str
    password: str

    @validator("username")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        return validate_phone_number(value)

    @validator("password")
    def validate_password(cls, value):  # pylint: disable=no-self-argument
        """
        Simple password
        """
        if 7 < len(value) < 129:
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
