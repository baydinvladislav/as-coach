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

nutrition_router = APIRouter(prefix="/nutrition")


# GET nutrition/diets/${customer_id}/${specific_day}
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


# наверное тут нужно передавать идентификаторы Meals, при создании каждой диеты тренером,
# мы должны создать связанные с диетой Meals, должно быть создано 4 таких записей: завтрак, обед, ужин, перекус
# POST nutrition/diets/${diet_id}/breakfast||lunch||dinner||snacks/${product_id}
@nutrition_router.post(
    "/diets",
    summary="Consume product inside diet",
    response_model=DailyDietOut,
    status_code=status.HTTP_201_CREATED)
async def consume_product_in_diet(
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
        response:
    """
    ...


# GET nutrition/products/${product_word}
@nutrition_router.get(
    "/products/lookup",
    summary="Get product by relative product word",
    # response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def find_product(
    query_text: str,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> dict:
    """
    Find product by relative product word

    Args:
        query_text: word for looking up in db
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    return {"test": "OK!"}


# POST nutrition/products
@nutrition_router.post(
    "/products",
    summary="Save new product to AsCoach product database",
    response_model=DailyDietOut,
    status_code=status.HTTP_201_CREATED)
async def put_product_in_catalog(
    customer_id: UUID,
    specific_day: date,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Save new product to AsCoach product database

    Args:
        customer_id: whose diet
        specific_day: date daily diet applying
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...


# GET nutrition/products/${product_id}
@nutrition_router.get(
    "/products",
    summary="Get specific product",
    response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def get_specific_product(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Get customer daily diet

    Args:
        product_id: id for specific product
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...


# DELETE nutrition/products/${product_id}
@nutrition_router.delete(
    "/products",
    summary="Get customer daily diet",
    response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def consume_product_in_diet(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Get customer daily diet

    Args:
        product_id: id for specific product
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...


# PUT nutrition/products/${product_id}
@nutrition_router.put(
    "/products",
    summary="Update product data",
    response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def consume_product_in_diet(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Get customer daily diet

    Args:
        product_id: id for specific product
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...
