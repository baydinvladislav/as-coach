"""
Dependencies for auth service trigger
during request to common API endpoints
"""

from typing import Union

from fastapi import Depends, HTTPException, status

from src.customer.models import Customer
from src.customer.dependencies import get_current_customer
from src.coach.models import Coach
from src.coach.dependencies import get_current_coach


async def get_current_user(
        coach: Coach = Depends(get_current_coach),
        customer: Customer = Depends(get_current_customer)
) -> Union[Coach, Customer]:
    """
    Provides current application user during request to common endpoints,
    if neither Coach nor Customer aren't found raises 404 error.
    Works through sub-dependencies from coach and customer application respectively.

    Args:
        coach: ORM obj for coach
        customer: ORM obj for customer

    Return:
        user: represented Coach or Customer ORM model
    """
    user = coach or customer

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    return user
