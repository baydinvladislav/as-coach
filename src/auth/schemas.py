from pydantic import BaseModel
from typing import NewType

from src.models import Gender


class UserAuth(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    gender: NewType('Gender', Gender)


class UserOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
