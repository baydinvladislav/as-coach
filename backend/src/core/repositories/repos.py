"""
Stores custom repositories for interaction with domains
"""

from src.coach.models import Coach
from src.customer.models import Customer, TrainingPlan
from src.gym.models import Diet, Training, DietOnTrainingPlan, ExercisesOnTraining
from src.core.repositories.sqlalchemy import SQLAlchemyRepository


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
