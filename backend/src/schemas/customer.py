"""
Schemas for customer service
"""

from typing import Optional, List, Union

from pydantic import BaseModel, validator

from src.utils import validate_phone_number
from src.schemas.library import Diet, Training


class CustomerCreateIn(BaseModel):
    """
    Schema to create new customer
    """
    first_name: str
    last_name: str
    phone_number: Optional[str]

    @validator("phone_number")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        if value is not None:
            return validate_phone_number(value)


class CustomerOut(CustomerCreateIn, BaseModel):
    """
    Schema represents Customer in response
    """
    id: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    last_plan_end_date: Union[str, None]


class CustomerRegistrationData(BaseModel):
    """
    DB schema before saving
    """
    coach_id: str
    coach_name: str
    username: str | None
    password: str
    first_name: str
    last_name: str


class TrainingPlanIn(BaseModel):
    """
    Income JSON for creating training plan for user
    """
    start_date: str
    end_date: str
    diets: List[Diet]
    trainings: List[Training]
    set_rest: int
    exercise_rest: int
    notes: Optional[str]


class TrainingPlanOut(BaseModel):
    """
    Output JSON after successfully training plan creation
    """
    id: str
    start_date: str
    end_date: str
    number_of_trainings: int
    proteins: str
    fats: str
    carbs: str


class ExerciseOut(BaseModel):
    id: str
    name: str
    sets: list
    superset_id: Optional[str]
    ordering: int


class TrainingOut(BaseModel):
    id: str
    name: str
    number_of_exercises: int
    exercises: list[ExerciseOut]


class TrainingPlanOutFull(BaseModel):
    """
    Full training plan data
    """
    id: str
    start_date: str
    end_date: str
    proteins: str
    fats: str
    carbs: str
    trainings: Optional[list[TrainingOut]]
    set_rest: int
    exercise_rest: int
    notes: Optional[str]
