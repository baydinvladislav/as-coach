from fastapi import HTTPException
from starlette import status

from src import Coach, Customer
from src.auth.utils import verify_password


def auth_coach(coach: Coach, password: str) -> bool:
    """
    Coach authorization

    Args:
        coach: coach SQLAlchemy obj
        password: password from front-end
    Raises:
        400 in case if coach exists but incorrect password was passed
    Returns:
        True in case successfully authorization
    """
    if verify_password(password, coach.password):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password for the coach"
        )


def auth_customer(customer: Customer, password: str) -> bool:
    """
    Customer authorization.
    The customer can have a default password or a hashed password

    Args:
        customer: customer SQLAlchemy obj
        password: password from front-end
    Raises:
        400 in case if coach exists but incorrect password was passed
    Returns:
        True in case successfully authorization
    """
    if customer.password == password \
            or verify_password(password, customer.password):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password for the customer"
        )
