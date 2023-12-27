"""
Schemas for auth routers
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from src.utils import validate_phone_number, validate_password
from src.persistence.models import Gender


class UserRegisterIn(BaseModel):
    """
    Schema for user registration
    """
    username: str
    password: str
    first_name: str
    fcm_token: str

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
    Response after success coach registration
    """
    id: str
    username: str
    first_name: str
    access_token: str
    refresh_token: str


class UserProfileOut(BaseModel):
    """
    Full user data for profile
    """
    id: str
    first_name: str
    last_name: Optional[str]
    gender: Optional[Gender]
    user_type: str
    birthday: Optional[date]
    email: Optional[str]
    username: Optional[str]
    photo_link: Optional[str]


class LoginOut(BaseModel):
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
    """
    Schema for changing user password
    """
    password: str

    @validator("password")
    def validate_password(cls, value):  # pylint: disable=no-self-argument
        """
        Simple password
        """
        return validate_password(value)
