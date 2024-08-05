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


class ScheduledExerciseDto(BaseModel):
    id: str
    name: str
    sets: None | list[int]
    superset_id: None | str
    ordering: int
