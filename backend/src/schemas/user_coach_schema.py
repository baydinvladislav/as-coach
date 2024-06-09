from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src import Gender


class UserCoachSchema(BaseModel):
    id: UUID
    username: str
    first_name: str
    fcm_token: str
    last_name: str | None
    password: str
    gender: Gender | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True


class UserCustomerSchema(BaseModel):
    id: UUID
    username: str | None
    first_name: str
    coach_id: UUID
    fcm_token: str
    last_name: str | None
    password: str
    telegram_username: str | None
    gender: Gender | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True


class UserCustomerShort(BaseModel):
    id: UUID
    first_name: str
    last_name: str | None
    username: str | None
    last_plan_end_date: date | None

    class Config:
        orm_mode = True
