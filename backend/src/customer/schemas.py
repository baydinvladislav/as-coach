"""
Schemas for customer service
"""

from typing import Optional

from pydantic import BaseModel, validator

from src.utils import validate_phone_number


class CustomerCreateIn(BaseModel):
    """
    Schema to create new customer
    """
    first_name: str
    last_name: str
    phone_number: Optional[str]

    @validator("phone_number")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        if value is not None:
            return validate_phone_number(value)


class CustomerOut(CustomerCreateIn, BaseModel):
    """
    Schema to response after successfully customer creation
    """
    id: str
