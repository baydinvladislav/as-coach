from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.diet_repository import DietRepository


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
