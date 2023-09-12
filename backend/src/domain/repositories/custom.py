"""
Stores custom repositories for interaction with domains
"""

from src import (
    Coach,
    Customer,
    TrainingPlan,
    Diet,
    DietOnTrainingPlan,
    Training,
    ExercisesOnTraining
)
from src.domain.repositories.sqlalchemy import SQLAlchemyRepository


class CoachRepository(SQLAlchemyRepository):
    """
    Access to Coach domain
    """
    model = Coach


class CustomerRepository(SQLAlchemyRepository):
    """
    Access to Customer domain
    """
    model = Customer


class TrainingPlanRepository(SQLAlchemyRepository):
    """
    Access to TrainingPlan domain
    """
    model = TrainingPlan


class TrainingRepository(SQLAlchemyRepository):
    """
    Access to Training domain
    """
    model = Training


class DietRepository(SQLAlchemyRepository):
    """
    Access to Diet domain
    """
    model = Diet


class DietOnTrainingPlanRepository(SQLAlchemyRepository):
    """
    Access to DietOnTrainingPlan domain
    """
    model = DietOnTrainingPlan


class ExercisesOnTrainingRepository(SQLAlchemyRepository):
    """
    Access to ExercisesOnTraining domain
    """
    model = ExercisesOnTraining
