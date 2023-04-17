"""
Schemas for gym service
"""

from typing import List

from pydantic import BaseModel


class Diet(BaseModel):
    """
    Diet in TrainingPlanIn
    """
    proteins: int
    fats: int
    carbs: int


class Exercise(BaseModel):
    """
    Exercise in TrainingPlanIn
    """
    id: str
    sets: List[int]


class Training(BaseModel):
    """
    Training in TrainingPlanIn
    """
    name: str
    exercises: List[Exercise]


class ExerciseCreateIn(BaseModel):
    """
    Schema for creating custom exercise
    """
    name: str
    muscle_group_id: str


class ExerciseCreateOut(BaseModel):
    """
    Schema for response after successfully creating custom exercise
    """
    id: str
    name: str
    muscle_group: str
