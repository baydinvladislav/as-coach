"""
Common dependencies for application
"""

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.database import SessionLocal
from src.service.library_service import LibraryService
from src.shared.config import reuseable_oauth
from src.utils import decode_jwt_token

from src.repository.library import ExerciseRepository, MuscleGroupRepository
from src.repository.diet import DietRepository, DietOnTrainingPlanRepository
from src.repository.training import TrainingRepository, ExercisesOnTrainingRepository
from src.repository.training_plan import TrainingPlanRepository
from src.repository.coach import CoachRepository
from src.repository.customer import CustomerRepository
from src.service.coach_service import CoachService, CoachProfileService, CoachSelectorService
from src.service.customer_service import CustomerService, CustomerSelectorService, CustomerProfileService
from src.supplier.kafka import KafkaSupplier, kafka_settings
from src.shared.exceptions import TokenExpired, NotValidCredentials
from src.service.training_plan_service import TrainingPlanService
from src.service.training_service import TrainingService
from src.service.diet_service import DietService
from src.service.notification_service import NotificationService
from src.supplier.firebase import PushFirebaseNotificator


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
    coach_repository = CoachRepository(database)
    profile_service = CoachProfileService(coach_repository)
    selector_service = CoachSelectorService(coach_repository)
    return CoachService(
        profile_service=profile_service,
        selector_service=selector_service,
    )


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


async def provide_push_notification_service() -> NotificationService:
    """
    Returns service responsible to send push notification through FireBase service
    """
    kafka_supplier = KafkaSupplier(
        topic=kafka_settings.customer_invite_topic, config={"bootstrap.servers": kafka_settings.bootstrap_servers}
    )
    firebase_supplier = PushFirebaseNotificator()
    return NotificationService(firebase_supplier, kafka_supplier)


async def provide_customer_service(
        database: Session = Depends(get_db),
        notification_service: NotificationService = Depends(provide_push_notification_service)
) -> CustomerService:
    """
    Returns service responsible to interact with Customer domain
    """
    customer_repository = CustomerRepository(database)
    selector = CustomerSelectorService(customer_repository)
    profile_service = CustomerProfileService(customer_repository)
    return CustomerService(
        selector_service=selector,
        profile_service=profile_service,
        notification_service=notification_service,
    )


async def provide_user_service(
        token: str = Depends(reuseable_oauth),
        coach_service: CoachService = Depends(provide_coach_service),
        customer_service: CustomerService = Depends(provide_customer_service)
) -> CoachService | CustomerService:
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

        coach = await coach_service.get_coach_by_username(username=username)
        customer = await customer_service.get_customer_by_username(username=username)

        if coach:
            return coach_service
        elif customer:
            return customer_service
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
