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
    id: UUID
    name: str
    exercise_id: UUID
    training_id: UUID
    sets: list[int]
    superset_id: None | UUID
    ordering: int

    class Config:
        orm_mode = True
