import logging
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.nutrition_schema import (
    DailyMealsOut,
    DailyDietOut,
    ProductOut,
    ProductToDietRequest,
)
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


@nutrition_router.get(
    "/diets/{specific_day}",
    summary="Get customer daily diet",
    response_model=DailyDietOut,
    status_code=status.HTTP_200_OK)
async def get_daily_diet(
    specific_day: date,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Get customer daily diet

    Args:
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
        customer_id=user.id,
        specific_day=specific_day,
    )

    if daily_diet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Daily diet for {user.id} today is not scheduled",
        )

    actual_nutrition = DailyMealsOut.from_diet_dto(daily_diet)

    return DailyDietOut(
        date=str(specific_day),
        actual_nutrition=actual_nutrition,
    )


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
    Add product to daily customer diet

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


# POST nutrition/products
@nutrition_router.post(
    "/products",
    summary="Save new product to AsCoach product database",
    response_model=DailyMealsOut,
    status_code=status.HTTP_201_CREATED)
async def put_product_in_catalog(
    customer_id: UUID,
    specific_day: date,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyMealsOut:
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
    summary="Get specific product from AsCoach product database by product_id",
    response_model=DailyMealsOut,
    status_code=status.HTTP_200_OK)
async def get_specific_product(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyMealsOut:
    """
    Get nutrition product from storage.

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
    summary="Delete product data from AsCoach product database",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK)
async def delete_product_from_storage(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyMealsOut:
    """
    Delete created by current customer product application storage.

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
    summary="Update product data in AsCoach product database",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK)
async def update_product_from_storage(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyMealsOut:
    """
    Update created by current customer product application storage.

    Args:
        product_id: id for updated product
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...


# GET nutrition/products/${query_text}
@nutrition_router.get(
    "/products/lookup",
    summary="Look up product by relative product word",
    response_model=list[ProductOut],
    status_code=status.HTTP_200_OK)
async def find_product(
    query_text: str,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> dict:
    """
    Find product by relative product word in application storage.

    Args:
        query_text: word for looking up in db
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    ...
