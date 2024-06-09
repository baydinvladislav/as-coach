from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src import Gender


class UserCoachSchema(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str | None
    password: str
    gender: Gender | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True
