"""
Contains every model related to the gym
"""

from sqlalchemy import Column, String, ForeignKey, Date, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
from src.models import BaseModel


class Diet(Base, BaseModel):
    """
    M2M to TrainingPlan
    """
    __tablename__ = "diet"

    proteins = Column("proteins", Integer, nullable=False)
    fats = Column("fats", Integer, nullable=False)
    carbs = Column("carbs", Integer, nullable=False)
    training_plans = relationship("TrainingPlan", secondary="dietontrainingplan", back_populates="diets")
    
    def __repr__(self):
        return f"diet: {self.proteins}/{self.fats}/{self.carbs}"


class DietOnTrainingPlan(Base, BaseModel):
    """
    Link table between Diet and TrainingsPlan tables
    """
    __tablename__ = "dietontrainingplan"

    nutrition_id = Column(UUID, ForeignKey("diet.id"), nullable=False)
    training_plan_id = Column(UUID, ForeignKey("trainingplan.id"), nullable=False)

    def __repr__(self):
        return f"diet on training plan: {self.id}"


class TrainingPlan(Base, BaseModel):
    """
    Contains training, nutrition and also relates to customer.
    """
    __tablename__ = "trainingplan"

    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    diets = relationship("Diet", secondary="dietontrainingplan", back_populates="training_plans")
    customer_id = Column(UUID, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="training_plans")
    trainings = relationship("Training", cascade="all,delete-orphan", back_populates="training_plan")

    def __repr__(self):
        return f"training_plan:  {self.start_date} до {self.end_date}"


class Training(Base, BaseModel):
    """
    Contains training's exercises.
    """
    __tablename__ = "training"

    name = Column("name", String(50), nullable=False)
    training_plan_id = Column(UUID, ForeignKey("trainingplan.id", ondelete="CASCADE"), nullable=False)
    training_plan = relationship("TrainingPlan", back_populates="trainings")
    exercises = relationship("Exercise", secondary="exercisesontraining", back_populates="trainings")

    def __repr__(self):
        return f"training: {self.name}"


class Exercise(Base, BaseModel):
    """
    Represents exercises in training.
    User can create custom exercises but user can not see custom exercises other users.
    """
    __tablename__ = "exercise"

    name = Column("name", String(50), nullable=False)
    trainings = relationship("Training", secondary="exercisesontraining", back_populates="exercises")
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="exercises")

    def __repr__(self):
        return f"exercise: {self.name}"


class ExercisesOnTraining(Base, BaseModel):
    """
    Model for M2M relationship Training and Exercise.
    """
    __tablename__ = "exercisesontraining"

    training_id = Column(UUID, ForeignKey("training.id"), nullable=False)
    exercise_id = Column(UUID, ForeignKey("exercise.id"), nullable=False)
    sets = Column('sets', JSON, default=[])

    def __repr__(self):
        return f"exercise on training: {self.id}"
