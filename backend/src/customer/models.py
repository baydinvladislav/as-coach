"""
Customer models.
"""

from sqlalchemy import Column, Enum, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
from src.models import Gender, BaseModel


class Customer(Base, BaseModel):
    """
    Customer, created by coach, gets training plan.
    """
    __tablename__ = "customer"
    __table_args__ = {'extend_existing': True}

    phone_number = Column("phone_number", String(100), nullable=True)
    password = Column("password", String, nullable=True)
    first_name = Column("first_name", String(50), nullable=False)
    last_name = Column("last_name", String(50), nullable=False)
    gender: Column = Column("gender", Enum(Gender), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="customers")

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"
