import logging
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.nutrition_schema import DailyDietOut
from src.service.coach_service import CoachService
from src.service.customer_service import CustomerService
from src.service.diet_service import DietService
from src.shared.dependencies import (
    provide_database_unit_of_work,
    provide_user_service,
    provide_diet_service,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

nutrition_router = APIRouter()


@nutrition_router.get(
    "/diets",
    summary="Get customer daily diet",
    response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def get_daily_diet(
    customer_id: UUID,
    specific_day: date,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Get customer daily diet

    Args:
        customer_id: whose diet
        specific_day: date daily diet applying
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response: daily customer diet
    """
    user = user_service.user

    daily_diet = await diet_service.get_daily_customer_diet(
        uow=uow,
        customer_id=customer_id,
        specific_day=specific_day,
    )
    response = DailyDietOut().from_daily_diet_dto(daily_diet)
    return response
