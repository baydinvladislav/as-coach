"""
Contains every model related to the gym
"""

from sqlalchemy import Column, String, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.src import Base
from backend.src.models import BaseModel


class Diet(Base, BaseModel):
    """
    M2M to TrainingPlan
    """
    __tablename__ = "diet"

    proteins = Column("proteins", Integer, nullable=False)
    fats = Column("fats", Integer, nullable=False)
    carbs = Column("carbs", Integer, nullable=False)
    training_plans = relationship(
        "TrainingPlan",
        secondary="dietontrainingplan",
        back_populates="diets"
    )
    
    def __repr__(self):
        return f"diet: {self.proteins}/{self.fats}/{self.carbs}"


class DietOnTrainingPlan(Base, BaseModel):
    """
    Link table between Diet and TrainingsPlan tables
    """
    __tablename__ = "dietontrainingplan"

    diet_id = Column(UUID, ForeignKey("diet.id"), nullable=False)
    training_plan_id = Column(UUID, ForeignKey("trainingplan.id"), nullable=False)

    def __repr__(self):
        return f"diet on training plan: {self.id}"


class Training(Base, BaseModel):
    """
    Contains training's exercises.
    """
    __tablename__ = "training"

    name = Column("name", String(50), nullable=False)
    training_plan_id = Column(
        UUID,
        ForeignKey("trainingplan.id", ondelete="CASCADE"),
        nullable=False
    )
    training_plan = relationship("TrainingPlan", back_populates="trainings")
    exercises = relationship(
        "Exercise",
        secondary="exercisesontraining",
        back_populates="trainings"
    )

    def __repr__(self):
        return f"training: {self.name}"


class MuscleGroup(Base, BaseModel):
    """
    Muscle group for exercises
    """
    __tablename__ = "musclegroup"

    name = Column("name", String(50), nullable=False)
    exercises = relationship(
        "Exercise",
        back_populates="muscle_group",
        cascade="all,delete-orphan"
    )


class Exercise(Base, BaseModel):
    """
    Represents exercises in training.
    User can create custom exercises
    but user can not see custom exercises other users.
    """
    __tablename__ = "exercise"

    name = Column("name", String(50), nullable=False)
    trainings = relationship(
        "Training",
        secondary="exercisesontraining",
        back_populates="exercises"
    )
    coach_id = Column(UUID, ForeignKey("coach.id"))
    coach = relationship("Coach", back_populates="exercises")
    muscle_group_id = Column(UUID, ForeignKey("musclegroup.id"), nullable=False)
    muscle_group = relationship("MuscleGroup", back_populates="exercises")

    def __repr__(self):
        return f"exercise: {self.name}"


class ExercisesOnTraining(Base, BaseModel):
    """
    Model for M2M relationship Training and Exercise.
    """
    __tablename__ = "exercisesontraining"

    training_id = Column(UUID, ForeignKey("training.id"), nullable=False)
    exercise_id = Column(UUID, ForeignKey("exercise.id"), nullable=False)
    sets = Column("sets", JSON, default=[])
    superset_id = Column(UUID, nullable=True)
    ordering = Column("ordering", Integer, default=0)

    def __repr__(self):
        return f"exercise on training: {self.id}"
