from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src import Diet, DietOnTrainingPlan


class DietRepository:
    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> int:
        uow.add_all(
            [Diet(proteins=diet.proteins, fats=diet.fats, carbs=diet.carbs, training_plan_id=training_plan_id)
             for diet in diets]
        )
        return len(diets)


# TODO: deprecated
class DietOnTrainingPlanRepository:
    model = DietOnTrainingPlan
