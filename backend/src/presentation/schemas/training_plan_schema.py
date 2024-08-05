from typing import List, Union, Optional

from pydantic import BaseModel


class DietIn(BaseModel):
    """
    Diet in TrainingPlanIn
    """
    proteins: int
    fats: int
    carbs: int


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


class ExerciseForCoachOut(BaseModel):
    id: str
    name: str
    muscle_group: str
    muscle_group_id: str


class ExerciseIn(BaseModel):
    """
    Exercise in TrainingPlanIn
    """
    id: str
    sets: List[int]
    supersets: Union[List[str], None]


class ExerciseOut(BaseModel):
    id: str
    name: str
    sets: list
    superset_id: Optional[str]
    ordering: int


class TrainingIn(BaseModel):
    """
    Training in TrainingPlanIn
    """
    name: str
    exercises: List[ExerciseIn]


class TrainingOut(BaseModel):
    id: str
    name: str
    number_of_exercises: int
    exercises: list[ExerciseOut]


class TrainingPlanIn(BaseModel):
    """
    Income JSON for creating training plan for user
    """
    start_date: str
    end_date: str
    diets: List[DietIn]
    trainings: List[TrainingIn]
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
