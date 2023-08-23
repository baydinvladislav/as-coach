"""
Dependencies for customer service triggered
during request to only for coach API endpoints
"""

from typing import Type

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.coach.models import Coach
from src.core.repositories.repos import CoachRepository, CustomerRepository
from src.core.services.coach import CoachService
from src.core.services.customer import CustomerService
from src.core.services.profile import ProfileService
from src.dependencies import get_db
from src.auth.utils import decode_jwt_token
from src.auth.config import reuseable_oauth


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
