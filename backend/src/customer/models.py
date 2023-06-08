"""
Customer models.
"""

from sqlalchemy import Column, Enum, String, ForeignKey, Date, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .. import Base
from .. import BaseModel, Gender


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
    coach_id = Column(UUID, ForeignKey("coach.id"), nullable=False)
    coach = relationship("Coach", back_populates="customers")
    training_plans = relationship(
        "TrainingPlan",
        cascade="all,delete-orphan",
        back_populates="customer"
    )
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)
    email = Column("email", String(100), nullable=True)
    
    # user = relationship("User", back_populates="customer")

    def __repr__(self):
        return f"customer: {self.last_name} {self.first_name}"


class TrainingPlan(Base, BaseModel):
    """
    Contains training, diets, notes and also relates to customer.
    """
    __tablename__ = "trainingplan"

    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    diets = relationship(
        "Diet",
        secondary="dietontrainingplan",
        back_populates="training_plans"
    )
    customer_id = Column(UUID, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="training_plans")
    trainings = relationship(
        "Training",
        cascade="all,delete-orphan",
        back_populates="training_plan"
    )
    notes = Column("notes", Text, nullable=True)
    set_rest = Column("set_rest", Integer, default=60)
    exercise_rest = Column("exercise_rest", Integer, default=120)

    def __repr__(self):
        return f"training_plan:  {self.start_date} до {self.end_date}"
