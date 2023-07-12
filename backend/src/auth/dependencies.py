"""
Dependencies for auth service trigger
during request to common API endpoints
"""

from typing import Union

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src.customer.models import Customer
from src.coach.models import Coach
from src.auth.utils import decode_jwt_token
from src.auth.config import reuseable_oauth
from src.dependencies import get_db


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        database: AsyncSession = Depends(get_db)
) -> Union[Coach, Customer]:
    """
    Provides current application user during request to common endpoints,
    if neither Coach nor Customer aren't found raises 404 error.

    Args:
        token: jwt token which contains user username
        database: dependency injection for access to database

    Return:
        user: represented Coach or Customer ORM model
    """
    token_data = await decode_jwt_token(token)
    token_username = token_data.sub

    coach = await database.execute(
        select(Coach).where(Coach.username == token_username)
    )
    customer = await database.execute(
        select(Customer).where(Customer.username == token_username)
    )

    user = coach.scalar() or customer.scalar()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find any user"
        )

    return user
