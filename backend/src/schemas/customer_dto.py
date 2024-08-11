from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src import Gender


class CustomerDtoSchema(BaseModel):
    id: UUID
    username: str | None
    first_name: str
    coach_id: UUID
    fcm_token: str | None
    last_name: str | None
    password: str
    telegram_username: str | None
    gender: Gender | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True


class CustomerShortDtoSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str | None
    username: str | None
    last_plan_end_date: date | None

    class Config:
        orm_mode = True
