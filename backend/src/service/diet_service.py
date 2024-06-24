from sqlalchemy.ext.asyncio import AsyncSession

from src import DietOnTrainingPlan
from src.repository.diet_repository import DietRepository, DietOnTrainingPlanRepository


class DietService:
    def __init__(self, diet_repository: DietRepository) -> None:
        self.diet_repository = diet_repository

    async def create_diets(self, uow: AsyncSession, training_plan_id: str, diets: list):
        diets = await self.diet_repository.create_diets(uow=uow, diets=diets)

        # bulk creation
        for diet_data in diets:
            diet = await self.diet_repository.create(
                uow=uow,
                proteins=diet_data.proteins,
                fats=diet_data.fats,
                carbs=diet_data.carbs
            )

            self.diet_repository.session.add(diet)
            await self.diet_repository.session.flush()

            diet_on_training_plan = DietOnTrainingPlan(
                diet_id=str(diet.id),
                training_plan_id=training_plan_id
            )
            self.diet_repository.session.add(diet_on_training_plan)
