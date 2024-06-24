from sqlalchemy.ext.asyncio import AsyncSession


from src import Diet, DietOnTrainingPlan
from src.schemas.diet_dto import DietDtoSchema


class DietRepository:
    async def create_diets(self, uow: AsyncSession, diets: list):
        a = await uow.bulk_save_objects(
            [Diet(proteins=diets[i], fats=diets[i], carbs=diets[i]) for i in range(len(diets))]
        )


class DietOnTrainingPlanRepository:
    model = DietOnTrainingPlan
