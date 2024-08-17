from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from src.utils import validate_password
from src.persistence.models import Gender


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
    username: str
    photo_link: Optional[str]


class CurrentUserOut(BaseModel):
    id: str
    user_type: str
    username: str | None
    first_name: str | None


class TokenPayload(BaseModel):
    """
    Validates token payload
    """
    sub: str
    exp: int


class NewUserPassword(BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, value):
        return validate_password(value)