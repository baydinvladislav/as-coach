from datetime import date

from pydantic import BaseModel

from src import Gender


class UserCoachSchema(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str | None
    user_type: str
    password_changed: bool
    gender: Gender | None
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True
