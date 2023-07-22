"""
Contains every model related to the gym
"""

from sqlalchemy import Column, String, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, RelationshipProperty

from .. import Base
from .. import BaseModel


class Diet(Base, BaseModel):
    """
    M2M to TrainingPlan
    """
    __tablename__ = "diet"

    proteins = Column("proteins", Integer, nullable=False)
    fats = Column("fats", Integer, nullable=False)
    carbs = Column("carbs", Integer, nullable=False)
    training_plans: RelationshipProperty = relationship(
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

    diet_id = Column(UUID(as_uuid=True), ForeignKey("diet.id"), nullable=False)
    training_plan_id = Column(UUID(as_uuid=True), ForeignKey("trainingplan.id"), nullable=False)

    def __repr__(self):
        return f"diet on training plan: {self.id}"


class Training(Base, BaseModel):
    """
    Contains training's exercises.
    """
    __tablename__ = "training"

    name = Column("name", String(50), nullable=False)
    training_plan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trainingplan.id", ondelete="CASCADE"),
        nullable=False
    )
    training_plan: RelationshipProperty = relationship("TrainingPlan", back_populates="trainings")
    exercises: RelationshipProperty = relationship(
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
    exercises: RelationshipProperty = relationship(
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
    trainings: RelationshipProperty = relationship(
        "Training",
        secondary="exercisesontraining",
        back_populates="exercises"
    )
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coach.id"))
    coach: RelationshipProperty = relationship("Coach", back_populates="exercises")
    muscle_group_id = Column(UUID(as_uuid=True), ForeignKey("musclegroup.id"), nullable=False)
    muscle_group: RelationshipProperty = relationship("MuscleGroup", back_populates="exercises")

    def __repr__(self):
        return f"Exercise: {self.name}"


class ExercisesOnTraining(Base, BaseModel):
    """
    Model for M2M relationship Training and Exercise.
    """
    __tablename__ = "exercisesontraining"

    training_id = Column(UUID(as_uuid=True), ForeignKey("training.id", ondelete="CASCADE"))
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="CASCADE"))
    sets = Column("sets", JSON, default=[])
    superset_id = Column(UUID(as_uuid=True), nullable=True)
    ordering = Column("ordering", Integer, default=0)

    def __repr__(self):
        return f"Exercise on training: {self.id}"
