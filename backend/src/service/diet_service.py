from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.diet_repository import DietRepository
from src.schemas.diet_dto import DailyDietDtoSchema


class DietService:
    def __init__(self, diet_repository: DietRepository) -> None:
        self.diet_repository = diet_repository

    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> int:
        inserted_row_amount = await self.diet_repository.create_diets(
            uow=uow,
            training_plan_id=training_plan_id,
            diets=diets,
        )
        return inserted_row_amount

    async def get_daily_customer_diet(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date,
    ) -> DailyDietDtoSchema | None:
        diet = await self.diet_repository.get_daily_diet(
            uow=uow,
            customer_id=customer_id,
            specific_day=specific_day,
        )
        return diet
