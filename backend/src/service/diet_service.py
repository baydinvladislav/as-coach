from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.training_plan_schema import DietIn
from src.repository.diet_repository import DietRepository
from src.schemas.diet_dto import DailyDietDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService


class DietService:
    def __init__(
        self,
        diet_repository: DietRepository,
        calories_calculator_service: CaloriesCalculatorService,
    ) -> None:
        self.diet_repository = diet_repository
        self.calories_calculator_service = calories_calculator_service

    @staticmethod
    async def _calculate_calories(proteins: int, fats: int, carbs: int) -> int:
        protein_coefficient = 4
        carb_coefficient = 4
        fat_coefficient = 9
        result = (proteins * protein_coefficient) + (carbs * carb_coefficient) + (fats * fat_coefficient)
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
        diet = await self.diet_repository.get_daily_diet(
            uow=uow,
            customer_id=customer_id,
            specific_day=specific_day,
        )
        return diet
