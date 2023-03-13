"""
Auth models folder.
"""

from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from src.models import Base, BaseModel, Gender


class User(Base, BaseModel):
    """
    Application user model.
    """
    username = Column("username", String(100), nullable=False)
    password = Column("password", String, nullable=False)
    first_name = Column("first_name", String(50), nullable=True)
    last_name = Column("last_name", String(50), nullable=True)
    gender: Column = Column("gender", Enum(Gender), nullable=True)

    # customers = relationship("Customer", cascade="all,delete-orphan", back_populates="user")
    # exercises = relationship("Exercise", cascade="all,delete-orphan", back_populates="user")
