from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.nutrition_schema import MealType, ProductAddInDiet
from src.presentation.schemas.training_plan_schema import DietIn
from src.repository.diet_repository import DietRepository
from src.schemas.diet_dto import DailyDietDtoSchema
from src.schemas.product_dto import ProductDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService
from src.service.product_service import ProductService


class DietService:
    def __init__(
        self,
        diet_repository: DietRepository,
        calories_calculator_service: CaloriesCalculatorService,
        product_service: ProductService,
    ) -> None:
        self.diet_repository = diet_repository
        self.calories_calculator_service = calories_calculator_service
        self.product_service = product_service

    async def actualize_daily_diet_fact(
        self,
        updating_daily_diet: DailyDietDtoSchema,
        meal_type: MealType,
        adding_products_data: list[ProductAddInDiet],
        products_info: list[ProductDtoSchema],
    ) -> tuple[DailyDietDtoSchema, dict]:
        merged_list = [
            {**product.dict(), **amount.dict()}
            for product, amount in zip(products_info, adding_products_data)
        ]

        updating_meal = getattr(updating_daily_diet, meal_type)
        for item in merged_list:
            updating_daily_diet.total_calories += item["calories"]
            updating_daily_diet.total_proteins += item["proteins"]
            updating_daily_diet.total_fats += item["fats"]
            updating_daily_diet.total_carbs += item["carbs"]

            updating_meal["total_calories"] += item["calories"]
            updating_meal["total_proteins"] += item["proteins"]
            updating_meal["total_fats"] += item["fats"]
            updating_meal["total_carbs"] += item["carbs"]
            updating_meal["products"].append(item)

        return updating_daily_diet, updating_meal

    async def put_product_to_diet_meal(
        self,
        uow: AsyncSession,
        diet_id: UUID,
        meal_type: MealType,
        adding_products_data: list[ProductAddInDiet],
        specific_day: str,
    ) -> DailyDietDtoSchema | None:
        products_full_info = await self.product_service.get_products_by_barcodes(
            barcodes=[item.barcode for item in adding_products_data],
        )
        updating_daily_diet = await self.diet_repository.get_daily_diet_by_diet_id_and_date(
            uow=uow,
            diet_id=diet_id,
            specific_day=specific_day,
        )
        updated_daily_diet, updated_meal = await self.actualize_daily_diet_fact(
            updating_daily_diet=updating_daily_diet,
            meal_type=meal_type,
            adding_products_data=adding_products_data,
            products_info=products_full_info,
        )
        result = await self.diet_repository.update_daily_diet_meal(
            uow=uow,
            updated_daily_diet=updated_daily_diet,
            meal_type=meal_type,
            updated_meal=updated_meal,
        )
        return result

    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list[DietIn]) -> int:
        for diet in diets:
            diet.calories = await self.calories_calculator_service.calculate_calories(
                proteins=diet.proteins,
                fats=diet.fats,
                carbs=diet.carbs,
            )

        diet_ids = await self.diet_repository.create_diets(
            uow=uow,
            training_plan_id=training_plan_id,
            diets=diets,
        )

        return len(diet_ids)

    async def get_daily_customer_diet(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date,
    ) -> DailyDietDtoSchema | None:
        diet = await self.diet_repository.get_daily_diet_by_training_plan_date_range(
            uow=uow,
            customer_id=customer_id,
            specific_day=specific_day,
        )
        return diet
