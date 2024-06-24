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
    sets: dict
    superset_id: UUID
    ordering: int
