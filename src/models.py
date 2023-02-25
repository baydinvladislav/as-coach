import uuid
import enum
import datetime

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, String, ForeignKey, Date, DateTime, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


@as_declarative()
class Base:
    """
    Base model class with common column.
    """
    __tablename__ = "common"

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created = Column("created", DateTime, default=datetime.datetime.now(), nullable=False)
    modified = Column("modified", DateTime)
    deleted = Column("deleted", DateTime)


class ExercisesOnTraining(Base):
    """
    Model for M2M relationship Training and Exercise.
    """
    training_id = Column(UUID, ForeignKey("training.id"), nullable=False)
    exercise_id = Column(UUID, ForeignKey("exercise.id"), nullable=False)
    sets = Column('sets', JSON, default=[])


class Exercise(Base):
    """
    Represents exercises in training.
    User can create custom exercises but user can not see custom exercises other users.
    """
    name = Column("name", String(50), nullable=False)
    trainings = relationship("Training", secondary="exercisesontraining", back_populates="exercises")
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="exercises")

    def __repr__(self):
        return f"Упражнение: {self.name}"


class Training(Base):
    """
    Contains training's exercises.
    """
    name = Column("name", String(50), nullable=False)
    training_plan_id = Column(UUID, ForeignKey("trainingplan.id", ondelete="CASCADE"), nullable=False)
    training_plan = relationship("TrainingPlan", back_populates="trainings")
    exercises = relationship("Exercise", secondary="exercisesontraining", back_populates="trainings")

    def __repr__(self):
        return f"Тренировка: {self.name}"


class TrainingPlan(Base):
    """
    Contains training, nutrition and also relates to customer.
    """
    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    proteins = Column("proteins", Integer, nullable=False)
    fats = Column("fats", Integer, nullable=False)
    carbs = Column("carbs", Integer, nullable=False)
    customer_id = Column(UUID, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="training_plans")
    trainings = relationship("Training", cascade="all,delete-orphan", back_populates="training_plan")

    def __repr__(self):
        return f"Тренировочный план: с {self.start_date} до {self.end_date}"


class Gender(enum.Enum):
    """
    Enum for selecting customer gender.
    """
    male = "male"
    female = "female"


class Customer(Base):
    """
    Model represents user's customer.
    """
    first_name = Column("first_name", String(50), nullable=False)
    last_name = Column("last_name", String(50), nullable=False)
    gender = Column("gender", Enum(Gender), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="customers")
    training_plans = relationship("TrainingPlan", cascade="all,delete-orphan", back_populates="customer")

    def __repr__(self):
        return f"Клиент: {self.first_name} {self.last_name}"


class User(Base):
    """
    Application user model.
    """
    name = Column("name", String(50), nullable=False)
    username = Column("username", String(100), nullable=False)
    password = Column("password", String, nullable=False)
    customers = relationship("Customer", cascade="all,delete-orphan", back_populates="user")
    exercises = relationship("Exercise", cascade="all,delete-orphan", back_populates="user")
    deleted = Column("deleted", Date)

    def __repr__(self):
        return f"Пользователь: {self.first_name} {self.last_name}"
