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
    HistoryProductOut,
)
from src.presentation.schemas.product_schema import ProductCreateIn, ProductCreateOut
from src.shared.exceptions import BarcodeAlreadyExistExc
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
    actual_nutrition = DailyMealsOut.from_diet_dto(daily_diet)
    return DailyDietOut(
        id=daily_diet.diet_day_id,
        date=str(specific_day),
        actual_nutrition=actual_nutrition,
    )


@nutrition_router.post(
    "/diets",
    summary="Consume products inside diet",
    response_model=DailyDietOut,
    status_code=status.HTTP_201_CREATED)
async def add_product_to_diet_meal(
    request: ProductToDietRequest,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    diet_service: DietService = Depends(provide_diet_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> DailyDietOut:
    """
    Add product to daily customer diet meal

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
        daily_diet_id=request.daily_diet_id,
        meal_type=request.meal_type,
        adding_products_data=request.product_data,
    )

    if updated_daily_diet is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"couldn't.update.customer.diet.meal {user.id=} {request.daily_diet_id=}",
        )

    actual_nutrition = DailyMealsOut.from_diet_dto(updated_daily_diet)
    return DailyDietOut(
        id=updated_daily_diet.diet_day_id,
        date=str(actual_nutrition.date),
        actual_nutrition=actual_nutrition,
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
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> ProductCreateOut:
    """
    Save new product to AsCoach product database

    Args:
        request: data for new product creation
        user_service: both user roles can access
        product_service: service to handle product domain
        uow: db session injection
    Returns:
        response:
    """
    user = user_service.user
    try:
        product = await product_service.create_product(
            uow=uow,
            user_id=user.id,
            product_data=request,
        )
    except BarcodeAlreadyExistExc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The product barcode already exists",
        )

    return ProductCreateOut(
        name=product.name,
        barcode=product.barcode,
        type=product.type,
        vendor_name=product.vendor_name,
        user_id=str(product.user_id),
        proteins=product.proteins,
        fats=product.fats,
        carbs=product.carbs,
        calories=product.calories,
    )


@nutrition_router.get(
    "/products/{barcode}",
    summary="Get specific product from AsCoach product database by product_id",
    response_model=ProductCreateOut,
    status_code=status.HTTP_200_OK)
async def get_specific_product_from_catalog(
    barcode: str,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    product_service: ProductService = Depends(provide_product_service),
) -> ProductCreateOut:
    """
    Get nutrition product from storage.

    Args:
        barcode: the product barcode
        user_service: both user roles can access
        product_service: service to handle product domain
    Returns:
        response:
    """
    user = user_service.user
    product = await product_service.get_product_by_barcode(barcode)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return ProductCreateOut(
        name=product.name,
        barcode=product.barcode,
        type=product.type,
        vendor_name=product.vendor_name,
        user_id=str(product.user_id),
        proteins=product.proteins,
        fats=product.fats,
        carbs=product.carbs,
        calories=product.calories,
    )


# DELETE nutrition/products/${product_id}
@nutrition_router.delete(
    "/products",
    summary="Delete product data from AsCoach product database",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK)
async def delete_product_from_catalog(
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
async def update_product_in_catalog(
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


@nutrition_router.get(
    "/products/lookup/{query_text}",
    summary="Look up product by relative product word",
    response_model=list[ProductOut],
    status_code=status.HTTP_200_OK)
async def find_product_in_catalog(
    query_text: str,
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    product_service: ProductService = Depends(provide_product_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> list[ProductOut]:
    """
    Find product by relative product word in application storage.

    Args:
        query_text: word for looking up in db
        user_service: both user roles can access
        product_service: service responsible for nutrition product logic
        uow: db session injection
    Returns:
        response: list of suitable products
    """
    user = user_service.user
    products_dto = await product_service.search_products(query_text)
    products_response = [
        ProductOut(
            barcode=p.barcode,
            name=p.name,
            type=p.type,
            proteins=p.proteins,
            fats=p.fats,
            carbs=p.carbs,
            calories=p.calories,
            vendor_name=p.vendor_name,
        ) for p in products_dto
    ]
    return products_response


@nutrition_router.get(
    "/products/history/all",
    summary="User consumed products history",
    response_model=list[HistoryProductOut],
    status_code=status.HTTP_200_OK)
async def get_user_products_history(
    user_service: CoachService | CustomerService = Depends(provide_user_service),
    product_service: ProductService = Depends(provide_product_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> list[HistoryProductOut]:
    """
    Find consumed products in customer history.

    Args:
        user_service: both user roles can access
        product_service: service responsible for nutrition product logic
        uow: db session injection
    Returns:
        response: recently consumed products by user
    """
    user = user_service.user
    product_history = await product_service.get_product_history(uow, user.id)
    products = [
        HistoryProductOut(
            name=ph.name,
            type=ph.type,
            proteins=ph.proteins,
            fats=ph.fats,
            carbs=ph.carbs,
            calories=ph.calories,
            vendor_name=ph.vendor_name,
            customer_id=ph.customer_id,
            barcode=ph.barcode,
            amount=ph.amount,
        )
        for ph
        in product_history
    ]
    return products
