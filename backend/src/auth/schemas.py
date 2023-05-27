"""
Schemas for auth service
"""

from datetime import date
from typing import NewType, Optional

from pydantic import BaseModel, validator

from src.utils import validate_phone_number
from src.auth.utils import validate_password
from src.models import Gender


class UserRegisterIn(BaseModel):
    """
    Schema for user registration
    """
    username: str
    password: str
    first_name: str

    @validator("username")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        return validate_phone_number(value)

    @validator("password")
    def validate_password(cls, value):  # pylint: disable=no-self-argument
        """
        Simple password
        """
        return validate_password(value)


class UserRegisterOut(BaseModel):
    """
    Response after success user registration
    """
    id: str
    username: str
    first_name: str
    access_token: str
    refresh_token: str


class UserProfile(BaseModel):
    """
    Full user data for profile
    """
    id: str
    first_name: str
    last_name: Optional[str]
    gender: Optional[NewType('Gender', Gender)]
    user_type: str
    birthday: Optional[date]
    email: Optional[str]
    username: Optional[str]
    photo_link: Optional[str]


class LoginResponse(BaseModel):
    """
    Response after successfully user login
    """
    id: str
    user_type: str
    first_name: str
    access_token: str
    refresh_token: str
    password_changed: bool


class TokenPayload(BaseModel):
    """
    Validates token payload
    """
    sub: str
    exp: int


class NewUserPassword(BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, value):  # pylint: disable=no-self-argument
        """
        Simple password
        """
        return validate_password(value)
