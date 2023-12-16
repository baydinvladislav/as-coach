"""
Common models folder.
"""

import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime, String, Enum, Date, ForeignKey, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import RelationshipProperty, relationship

from src import Base


class BaseModel:
    """
    Base model class with common column.
    """
    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created = Column("created", DateTime, default=datetime.datetime.now(), nullable=False)
    modified = Column("modified", DateTime)
    deleted = Column("deleted", DateTime)


class Gender(enum.Enum):
    """
    Enum for selecting customer gender.
    """
    MALE = "male"
    FEMALE = "female"


class Coach(Base, BaseModel):
    """
    Application user model.
    """
    __tablename__ = "coach"
    __table_args__ = {"extend_existing": True}

    username = Column("username", String(100), nullable=False)
    password = Column("password", String, nullable=False)
    first_name = Column("first_name", String(50), nullable=True)
    last_name = Column("last_name", String(50), nullable=True)
    gender: Column = Column("gender", Enum(Gender), nullable=True)
    customers: RelationshipProperty = relationship(
        "Customer",
        cascade="all,delete-orphan",
        back_populates="coach"
    )
    email = Column("email", String(100), nullable=True)
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)
    exercises: RelationshipProperty = relationship(
        "Exercise",
        cascade="all,delete-orphan",
        back_populates="coach"
    )
    # TODO: nullable False
    fcm_token = Column("fcm_token", String(255), nullable=True)

    def __repr__(self):
        return f"Coach: {self.username}"


class Customer(Base, BaseModel):
    """
    Customer, created by coach, gets training plan.
    """
    __tablename__ = "customer"
    __table_args__ = {'extend_existing': True}

    username = Column("username", String(100), nullable=True)
    password = Column("password", String, nullable=True)
    first_name = Column("first_name", String(50), nullable=False)
    last_name = Column("last_name", String(50), nullable=False)
    gender: Column = Column("gender", Enum(Gender), nullable=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coach.id", ondelete="CASCADE"))
    coach: RelationshipProperty = relationship("Coach", back_populates="customers")
    training_plans: RelationshipProperty = relationship(
        "TrainingPlan",
        cascade="all,delete-orphan",
        back_populates="customer"
    )
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)
    email = Column("email", String(100), nullable=True)
    # TODO: nullable False
    fcm_token = Column("fcm_token", String(255), nullable=True)

    def __repr__(self):
        return f"Customer: {self.last_name} {self.first_name}"


class TrainingPlan(Base, BaseModel):
    """
    Contains training, diets, notes and also relates to customer.
    """
    __tablename__ = "trainingplan"

    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    diets: RelationshipProperty = relationship(
        "Diet",
        secondary="dietontrainingplan",
        back_populates="training_plans"
    )
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id", ondelete="CASCADE"))
    customer: RelationshipProperty = relationship("Customer", back_populates="training_plans")
    trainings: RelationshipProperty = relationship(
        "Training",
        cascade="all,delete-orphan",
        back_populates="training_plan"
    )
    notes = Column("notes", Text, nullable=True)
    set_rest = Column("set_rest", Integer, default=60)
    exercise_rest = Column("exercise_rest", Integer, default=120)

    def __repr__(self):
        return f"Training_plan:  from {self.start_date} to {self.end_date}"


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

    diet_id = Column(UUID(as_uuid=True), ForeignKey("diet.id", ondelete="CASCADE"))
    training_plan_id = Column(UUID(as_uuid=True), ForeignKey("trainingplan.id", ondelete="CASCADE"))

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
    training_plan: RelationshipProperty = relationship(
        "TrainingPlan",
        back_populates="trainings"
    )
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
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coach.id", ondelete="CASCADE"))
    coach: RelationshipProperty = relationship("Coach", back_populates="exercises")
    muscle_group_id = Column(UUID(as_uuid=True), ForeignKey("musclegroup.id"), nullable=False)
    muscle_group: RelationshipProperty = relationship("MuscleGroup", back_populates="exercises")
    trainings: RelationshipProperty = relationship(
        "Training",
        secondary="exercisesontraining",
        back_populates="exercises"
    )

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
