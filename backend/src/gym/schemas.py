"""

"""

from typing import List

from pydantic import BaseModel


class Diet(BaseModel):
    """
    """
    proteins: int
    fats: int
    carbs: int


class Exercise(BaseModel):
    """
    """
    id: str
    sets: List[int]


class Training(BaseModel):
    """
    """
    name: str
    exercises: List[Exercise]
