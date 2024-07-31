from uuid import UUID

from pydantic import BaseModel


class ExerciseShortDtoSchema(BaseModel):
    id: UUID
    name: str
    coach_id: UUID | None

    class Config:
        orm_mode = True


class ExerciseFullDtoSchema(ExerciseShortDtoSchema):
    muscle_group_id: UUID
    muscle_group_name: str

    class Config:
        orm_mode = True
