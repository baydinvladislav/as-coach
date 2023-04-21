"""
Common models folder.
"""

import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


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


# TODO: merge two user models to one model
# class User(Base, BaseModel):
#     """
#     This is the main application user model,
#     Coach and Customer models will reference on it
#     one to one relation
#     """
#     __tablename__ = "user"
#     __table_args__ = {'extend_existing': True}
