from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src import Gender


class CoachDtoSchema(BaseModel):
    id: UUID
    username: str
    first_name: str
    fcm_token: str
    last_name: str | None
    password: str
    gender: str | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True
