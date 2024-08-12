from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src import Diet


class DietRepository:
    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> int:
        diet_orm = [
            Diet(
                proteins=diet.proteins,
                fats=diet.fats,
                carbs=diet.carbs,
                training_plan_id=training_plan_id,
            )
            for diet in diets
        ]

        uow.add_all(diet_orm)
        await uow.flush()

        return len(diets)
