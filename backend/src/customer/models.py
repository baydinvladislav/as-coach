"""
Customer models.
"""

from sqlalchemy import (
    Column,
    Enum,
    String,
    ForeignKey,
    Date,
    Text,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, RelationshipProperty

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
