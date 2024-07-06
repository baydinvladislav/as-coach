from uuid import UUID

from pydantic import BaseModel


class ExerciseDtoDto(BaseModel):
    id: UUID
    name: str
    coach_id: str | None

    class Config:
        orm_mode = True
