"""
Auth models folder.
"""

from sqlalchemy import Column, Enum, String, Date
from sqlalchemy.orm import relationship

from src.database import Base
from src.models import BaseModel, Gender


class User(Base, BaseModel):
    """
    Application user model.
    """
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    username = Column("username", String(100), nullable=False)
    password = Column("password", String, nullable=False)
    first_name = Column("first_name", String(50), nullable=True)
    last_name = Column("last_name", String(50), nullable=True)
    gender: Column = Column("gender", Enum(Gender), nullable=True)
    customers = relationship("Customer", cascade="all,delete-orphan", back_populates="user")
    email = Column("email", String(100), nullable=True)
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)

    def __repr__(self):
        return f"user: {self.username}"
