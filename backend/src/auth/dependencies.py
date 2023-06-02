"""
Dependencies for auth service trigger
during request to common API endpoints
"""

from typing import Type

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.customer.models import Customer
from src.coach.models import Coach
from src.auth.utils import decode_jwt_token
from src.auth.config import reuseable_oauth
from src.dependencies import get_db


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)
) -> Type[Coach | Customer]:
    """
    Provides current application user during request to common endpoints,
    if neither Coach nor Customer aren't found raises 404 error.

    Args:
        token: jwt token which contains user username
        database: dependency injection for access to database

    Return:
        user: represented Coach or Customer ORM model
    """
    token_data = decode_jwt_token(token)
    token_username = token_data.sub
    coach = database.query(Coach).filter(Coach.username == token_username).first()
    customer = database.query(Customer).filter(Customer.username == token_username).first()

    if coach is None and customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find any user"
        )

    return coach or customer
