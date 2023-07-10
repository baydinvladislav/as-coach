from fastapi import HTTPException
from starlette import status

from src.auth.utils import verify_password


async def auth_coach(hashed_password: str, passed_password: str) -> bool:
    """
    Coach authorization

    Args:
        hashed_password: current hashed password
        passed_password: password from client
    Raises:
        400 in case if coach exists but incorrect password was passed
    Returns:
        True in case successfully authorization
    """
    if await verify_password(passed_password, hashed_password):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password for the coach"
        )


async def auth_customer(hashed_password: str, passed_password: str) -> bool:
    """
    Customer authorization.
    The customer can have a default password or a hashed password

    Args:
        hashed_password: current hashed password
        passed_password: password from client
    Raises:
        400 in case if coach exists but incorrect password was passed
    Returns:
        True in case successfully authorization
    """
    if hashed_password == passed_password \
            or await verify_password(passed_password, hashed_password):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password for the customer"
        )
