"""
Dependencies for customer service
"""

from typing import Union
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.auth.models import User
from src.customer.models import Customer
from src.auth.schemas import TokenPayload
from src.auth.config import ALGORITHM, JWT_SECRET_KEY
from src.dependencies import get_db

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_coach_or_customer(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)) -> Union[User, Customer]:
    """
    Provide endpoint permission for coach and customer

    Extracts username from client token,
    provides current user
    """
    try:
        payload = jwt.decode(
            token, str(JWT_SECRET_KEY), algorithms=[str(ALGORITHM)]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except (jwt.JWTError, ValidationError):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_username = token_data.sub

    coach = database.query(User).filter(User.username == token_username).first()
    customer = database.query(Customer).filter(Customer.username == token_username).first()

    if coach is None and customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    return coach or customer
