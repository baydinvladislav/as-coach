"""

"""

from typing import Optional

from pydantic import BaseModel, validator

from src.utils import validate_phone_number


class CustomerCreateIn(BaseModel):
    """
    """
    first_name: str
    last_name: str
    phone_number: Optional[str]

    @validator("phone_number")
    def validate_phone_number(cls, value):  # pylint: disable=no-self-argument
        return validate_phone_number(value)


class CustomerCreateOut(CustomerCreateIn, BaseModel):
    """
    """
    id: str
