from datetime import date
from uuid import UUID

from pydantic import BaseModel, validator

from src import Gender


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
    @validator("gender", pre=True, always=True)
    def lowercase_gender(cls, gender_enum: Gender | None) -> str | None:
        if gender_enum is not None:
            return gender_enum.value.lower()
        return None
