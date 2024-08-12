from pydantic import BaseModel

from src.schemas.exercise_dto import ExerciseShortDtoSchema, ScheduledExerciseDto


class TrainingDtoSchema(BaseModel):
    id: str
    name: str
    exercises: list[ExerciseShortDtoSchema | ScheduledExerciseDto]
    number_of_exercises: int

    class Config:
        orm_mode = True
