"""
Dependencies for customer service
"""

from typing import Type

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.src.customer.models import Customer
from backend.src.dependencies import get_db
from backend.src.auth.utils import decode_jwt_token
from backend.src.auth.config import reuseable_oauth


async def get_current_customer(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)
) -> Type[Customer]:
    """
    Provides current customer during request to only customer's API endpoints

    Args:
        token: jwt token which contains user username
        database: dependency injection for access to database

    Return:
        customer: Customer ORM obj or None if customer wasn't found
    """
    token_data = decode_jwt_token(token)
    token_username = token_data.sub
    customer = database.query(Customer).filter(Customer.username == token_username).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer
