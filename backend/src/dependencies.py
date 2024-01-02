"""
Common dependencies for application
"""

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from sqlalchemy.orm import Session
from starlette import status

from src.database import SessionLocal
from src.service.library import LibraryService
from src.config import reuseable_oauth
from src.utils import decode_jwt_token

from src.repository.custom import (
    CoachRepository,
    CustomerRepository,
    TrainingPlanRepository,
    TrainingRepository,
    DietRepository,
    DietOnTrainingPlanRepository,
    ExercisesOnTrainingRepository,
    ExerciseRepository,
    MuscleGroupRepository
)
from src.service.authentication.coach import CoachService
from src.service.authentication.customer import CustomerService
from src.service.authentication.exceptions import TokenExpired, NotValidCredentials
from src.service.training_plan import TrainingPlanService
from src.service.training import TrainingService
from src.service.diet import DietService
from src.service.notifications.notification_service import NotificationService
from src.service.notifications.push_firebase_notificator import PushFirebaseNotificator


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


async def provide_library_service(database: Session = Depends(get_db)) -> LibraryService:
    """
    Returns service to organize data in gym library
    """
    return LibraryService(
        repositories={
            "exercise": ExerciseRepository(database),
            "muscle_group": MuscleGroupRepository(database)
        }
    )


async def provide_training_plan_service(database: Session = Depends(get_db)) -> TrainingPlanService:
    """
    Returns service responsible to interact with TrainingPlan domain
    """
    training_service = TrainingService(
        repositories={
            "training_repo": TrainingRepository(database),
            "exercises_on_training_repo": ExercisesOnTrainingRepository(database)
        }
    )
    diet_service = DietService(
        repositories={
            "diet_repo": DietRepository(database),
            "diets_on_training_repo": DietOnTrainingPlanRepository(database)
        }
    )
    return TrainingPlanService({"training_plan": TrainingPlanRepository(database)}, training_service, diet_service)


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
            detail="Not valid credentials"
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
                detail="User not found"
            )


async def provide_push_notification_service() -> NotificationService:
    """
    Returns service responsible to send push notification through FireBase service
    """
    return NotificationService(PushFirebaseNotificator())
