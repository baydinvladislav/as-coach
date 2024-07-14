from uuid import UUID

from pydantic import BaseModel

from src.schemas.exercise_dto import ExerciseDtoSchema


class TrainingDtoSchema(BaseModel):
    id: UUID
    name: str
    exercises: list[ExerciseDtoSchema]

    class Config:
        orm_mode = True


class ScheduleExercisesDtoSchema(BaseModel):
    id: UUID
    exercise_id: UUID
    training_id: UUID
    sets: list
    superset_id: UUID | None
    ordering: int

    class Config:
        orm_mode = True