from typing import Optional

from pydantic import BaseModel


class CustomerCreateIn(BaseModel):
    """
    Schema to create new customer
    """
    first_name: str
    last_name: str
    phone_number: Optional[str]


class CustomerOut(CustomerCreateIn, BaseModel):
    """
    Schema represents Customer in response
    """
    id: str
    first_name: str
    last_name: str
    phone_number: str | None
    last_plan_end_date: str | None
