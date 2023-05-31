"""
Dependencies for customer service
"""

from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.customer.models import Customer
from src.dependencies import get_db
from src.auth.utils import decode_jwt_token

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_current_customer(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)
) -> Union[Customer, None]:
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
    return customer
