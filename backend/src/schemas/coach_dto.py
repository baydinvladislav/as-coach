from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src import Coach, Gender


class CoachDtoSchema(BaseModel):
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

    @classmethod
    def from_coach_dto(cls, coach_row: Coach) -> "CoachDtoSchema":
        return cls(
            id=coach_row.id,
            username=coach_row.username,
            first_name=coach_row.first_name,
            last_name=coach_row.last_name,
            fcm_token=coach_row.fcm_token,
            password=coach_row.password,
            gender=coach_row.gender.value.lower() if coach_row.gender else None,
            birthday=coach_row.birthday,
            email=coach_row.email,
            photo_link=coach_row.photo_path,
        )
