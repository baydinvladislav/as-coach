from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src.schemas.diet_dto import DietDtoSchema
from src.schemas.training_dto import TrainingDtoSchema


class TrainingPlanDtoShortSchema(BaseModel):
    id: UUID
    start_date: date
    end_date: date
    number_of_trainings: int
    diets: list[DietDtoSchema]

    class Config:
        orm_mode = True


class TrainingPlanDtoSchema(BaseModel):
    id: UUID
    start_date: date
    end_date: date
    customer_id: UUID
    diets: list[DietDtoSchema]
    set_rest: int
    exercise_rest: int
    notes: str | None
    trainings: list[TrainingDtoSchema]

    class Config:
        orm_mode = True


class TrainingPlanDetailDtoSchema(BaseModel):
    id: str
    start_date: str
    end_date: str
    proteins: str
    fats: str
    carbs: str
    calories: int
    trainings: list[TrainingDtoSchema]
    set_rest: int
    exercise_rest: int
    notes: str | None
