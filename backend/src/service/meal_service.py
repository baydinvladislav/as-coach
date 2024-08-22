from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.meal_repository import MealRepository


class MealService:
    def __init__(self, meal_repository: MealRepository) -> None:
        self.meal_repository = meal_repository

    async def create_empty_meals(self, uow: AsyncSession, diet_ids: list[UUID]) -> int:
        inserted_rows_len = await self.meal_repository.insert_empty_meals(uow, diet_ids)
        return inserted_rows_len
