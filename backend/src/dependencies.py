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
from src.config import reuseable_oauth
from src.utils import decode_jwt_token

from src.domain.repositories.custom import (
    CoachRepository,
    CustomerRepository,
    TrainingPlanRepository,
    TrainingRepository,
    DietRepository,
    DietOnTrainingPlanRepository,
    ExercisesOnTrainingRepository
)
from src.application.services.coach import CoachService
from src.application.services.customer import CustomerService
from src.application.services.exceptions import TokenExpired, NotValidCredentials
from src.application.services.gym import Gym, GymInstructor, Nutritionist
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


async def provide_coach_service(database: Session = Depends(get_db)) -> CoachService:
    """
    Returns service responsible to interact with Coach domain
    """
    return CoachService(CoachRepository(database))


async def provide_customer_service(database: Session = Depends(get_db)) -> CustomerService:
    """
    Returns service responsible to interact with Customer domain
    """
    return CustomerService(CustomerRepository(database))


async def provide_gym_service(database: Session = Depends(get_db)) -> Gym:
    """
    Returns service responsible to interact with TrainingPlan domain
    """
    gym_instructor = GymInstructor(
        repositories={
            "training_repo": TrainingRepository(database),
            "exercises_on_training_repo": ExercisesOnTrainingRepository(database)
        }
    )
    nutritionist = Nutritionist(
        repositories={
            "diet_repo": DietRepository(database),
            "diets_on_training_repo": DietOnTrainingPlanRepository(database)
        }
    )
    return Gym({"training_plan": TrainingPlanRepository(database)}, gym_instructor, nutritionist)


async def provide_user_service(
        token: str = Depends(reuseable_oauth),
        coach_service: CoachService = Depends(provide_coach_service),
        customer_service: CustomerService = Depends(provide_customer_service)
):
    """
    Checks that token from client request is valid

    Args:
        token: token from client request
        coach_service: service for interacting with coach profile
        customer_service: service for interacting with customer profile

    Raises:
        401: HTTPException: in case if token is expired
        400: HTTPException: in case if credentials are not valid

    Return:
        username: username from token in case if it valid
    """
    try:
        token_data = await decode_jwt_token(token)
    except TokenExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except NotValidCredentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not valid credentials"
        )
    else:
        username = token_data.sub

        coach = await coach_service.find({"username": username})
        customer = await customer_service.find({"username": username})

        if coach:
            return coach_service
        elif customer:
            return customer_service
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found"
            )


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
