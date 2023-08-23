"""
Common dependencies for application
"""

from typing import Type, Union

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from sqlalchemy.orm import Session, selectinload
from starlette import status

from src import Coach, Customer
from src.auth.config import reuseable_oauth
from src.auth.utils import decode_jwt_token

from src.core.repositories.repos import CoachRepository, CustomerRepository
from src.core.services.coach import CoachService
from src.core.services.customer import CustomerService
from src.core.services.profile import ProfileService

from src.database import SessionLocal


async def get_db() -> AsyncSession:
    """
    Creates new database session.
    """
    async with SessionLocal() as database:
        try:
            yield database
        finally:
            await database.close()


async def get_coach_service(database: Session = Depends(get_db)) -> CoachService:
    """
    Returns service responsible to interact with Coach domain
    """
    return CoachService(CoachRepository(database))


async def get_customer_service(database: Session = Depends(get_db)) -> CustomerService:
    """
    Returns service responsible to interact with Customer domain
    """
    return CustomerService(CustomerRepository(database))


async def get_profile_service(
        coach_service: CoachService = Depends(get_coach_service),
        customer_service: CustomerService = Depends(get_customer_service),
) -> ProfileService:
    """
    Returns service responsible for user profile operations
    """
    return ProfileService(coach_service, customer_service)


async def get_current_coach(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)
) -> Type[Coach]:
    """
    Provides current coach during request to only coach's API endpoints

    Args:
        token: jwt token which contains user username
        database: dependency injection for access to database

    Return:
        coach: Coach ORM obj or None if coach wasn't found
    """

    token_data = await decode_jwt_token(token)
    token_username = token_data.sub

    coach = await database.execute(
        select(Coach).where(Coach.username == token_username).options(
            selectinload(Coach.customers).subqueryload('training_plans')
        )
    )
    coach = coach.scalar()

    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )

    return coach


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
