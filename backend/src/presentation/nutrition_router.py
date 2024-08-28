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
from src.presentation.schemas.product_schema import ProductCreateIn, ProductCreateOut
from src.service.coach_service import CoachService
from src.service.customer_service import CustomerService
from src.service.diet_service import DietService
from src.service.product_service import ProductService
from src.shared.dependencies import (
    provide_database_unit_of_work,
    provide_user_service,
    provide_diet_service,
    provide_product_service,
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
async def add_product_to_diet(
    request: ProductToDietRequest,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Add product to daily customer diet

    Args:
        request: request body with parameters
        user_service: both user roles can access
        diet_service: service responsible for customer diets
        uow: db session injection
    Returns:
        response:
    """
    user = user_service.user

    updated_daily_diet = await diet_service.put_product_to_diet_meal(
        uow=uow,
        diet_id=request.diet_id,
        meal_type=request.meal_type,
        product_id=request.product_id,
        product_amount=request.product_amount,
        specific_day=request.specific_day,
    )

    if updated_daily_diet is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"couldn't.update.customer.diet {user.id=} {request.diet_id=} {request.specific_day=}",
        )

    return DailyDietOut(
        date=request.specific_day,
        actual_nutrition=DailyMealsOut.from_diet_dto(updated_daily_diet),
    )


@nutrition_router.post(
    "/products",
    summary="Save new product to AsCoach product database",
    response_model=ProductCreateOut,
    status_code=status.HTTP_201_CREATED)
async def put_product_in_catalog(
    request: ProductCreateIn,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    product_service: ProductService = Depends(provide_product_service),
) -> ProductCreateOut:
    """
    Save new product to AsCoach product database

    Args:
        request: data for new product creation
        user_service: both user roles can access
        product_service: service to handle product domain
    Returns:
        response:
    """
    user = user_service.user
    product = await product_service.create_product(user.id, request)
    return ProductCreateOut(
        id=str(product.id),
        calories=product.calories,
        user_id=str(product.user_id),
        name=product.name,
        barcode=product.barcode,
        product_type=product.product_type,
        proteins=product.proteins,
        fats=product.fats,
        carbs=product.carbs,
        vendor_name=product.vendor_name,
    )


@nutrition_router.get(
    "/products/{product_id}",
    summary="Get specific product from AsCoach product database by product_id",
    response_model=ProductCreateOut,
    status_code=status.HTTP_200_OK)
async def get_specific_product(
    product_id: UUID,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    product_service: ProductService = Depends(provide_product_service),
) -> ProductCreateOut:
    """
    Get nutrition product from storage.

    Args:
        product_id: id for specific product
        user_service: both user roles can access
        product_service: service to handle product domain
    Returns:
        response:
    """
    user = user_service.user
    product = await product_service.get_product_by_id(product_id)
    return ProductCreateOut(
        id=str(product.id),
        calories=product.calories,
        user_id=str(product.user_id),
        name=product.name,
        barcode=product.barcode,
        product_type=product.product_type,
        proteins=product.proteins,
        fats=product.fats,
        carbs=product.carbs,
        vendor_name=product.vendor_name,
    )


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
