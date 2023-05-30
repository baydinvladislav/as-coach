"""
Dependencies for customer service
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.models import Coach
from src.customer.models import Customer
from src.dependencies import get_db
from src.auth.utils import decode_jwt_token

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_coach_or_customer(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)):
    """
    Provide endpoint permission for coach and customer

    Extracts username from client token,
    provides current user
    """
    token_data = decode_jwt_token(token)
    token_username = token_data.sub

    coach = database.query(Coach).filter(Coach.username == token_username).first()
    customer = database.query(Customer).filter(Customer.username == token_username).first()

    if coach is None and customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    return coach or customer
