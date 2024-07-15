from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import SessionLocal
from src.service.library_service import LibraryService
from src.shared.config import reuseable_oauth
from src.utils import decode_jwt_token
from src.repository.library_repository import ExerciseRepository, MuscleGroupRepository
from src.repository.diet_repository import DietRepository
from src.repository.training_repository import TrainingRepository
from src.repository.training_plan_repository import TrainingPlanRepository
from src.repository.coach_repository import CoachRepository
from src.repository.customer_repository import CustomerRepository
from src.service.coach_service import CoachService, CoachProfileService, CoachSelectorService
from src.service.customer_service import CustomerService, CustomerSelectorService, CustomerProfileService
from src.supplier.kafka_supplier import KafkaSupplier, kafka_settings
from src.shared.exceptions import TokenExpired, NotValidCredentials
from src.service.training_plan_service import TrainingPlanService
from src.service.training_service import TrainingService
from src.service.diet_service import DietService
from src.service.notification_service import NotificationService
from src.supplier.firebase_supplier import PushFirebaseNotificator


async def provide_database_unit_of_work() -> AsyncSession:
    async with SessionLocal() as unit_of_work:
        try:
            yield unit_of_work
        finally:
            await unit_of_work.close()


async def provide_coach_service() -> CoachService:
    coach_repository = CoachRepository()
    profile_service = CoachProfileService(coach_repository)
    selector_service = CoachSelectorService(coach_repository)
    return CoachService(profile_service=profile_service, selector_service=selector_service)


async def provide_library_service() -> LibraryService:
    return LibraryService(exercise_repository=ExerciseRepository(), muscle_group_repository=MuscleGroupRepository())


async def provide_training_plan_service() -> TrainingPlanService:
    return TrainingPlanService(
        training_plan_repository=TrainingPlanRepository(),
        training_service=TrainingService(TrainingRepository()),
        diet_service=DietService(DietRepository()),
    )


async def provide_push_notification_service() -> NotificationService:
    kafka_supplier = KafkaSupplier(
        topic=kafka_settings.customer_invite_topic, config={"bootstrap.servers": kafka_settings.bootstrap_servers}
    )
    firebase_supplier = PushFirebaseNotificator()
    return NotificationService(firebase_supplier, kafka_supplier)


async def provide_customer_service(
    notification_service: NotificationService = Depends(provide_push_notification_service)
) -> CustomerService:
    customer_repository = CustomerRepository()
    return CustomerService(
        selector_service=CustomerSelectorService(customer_repository),
        profile_service=CustomerProfileService(customer_repository),
        notification_service=notification_service,
    )


async def provide_user_service(
    uow: AsyncSession = Depends(provide_database_unit_of_work),
    token: str = Depends(reuseable_oauth),
    coach_service: CoachService = Depends(provide_coach_service),
    customer_service: CustomerService = Depends(provide_customer_service),
) -> CoachService | CustomerService:
    """
    Checks that token from client request is valid

    Args:
        uow: db session injection
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

        coach = await coach_service.get_coach_by_username(uow, username=username)
        customer = await customer_service.get_customer_by_username(uow, username=username)

        if coach:
            return coach_service
        elif customer:
            return customer_service
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
