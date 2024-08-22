from datetime import date
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src import Diet, TrainingPlan, Meal
from src.schemas.diet_dto import DailyDietDtoSchema


class DietRepository:
    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> list[UUID]:
        diet_orm = [
            Diet(
                proteins=diet.proteins,
                fats=diet.fats,
                carbs=diet.carbs,
                calories=diet.calories,
                training_plan_id=training_plan_id,
            )
            for diet in diets
        ]

        uow.add_all(diet_orm)
        await uow.flush()

        return diet_orm

    async def get_daily_diet(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date
    ) -> DailyDietDtoSchema | None:
        # TODO: этот подзапрос вернёт диету, теперь же нужно получить приемы диеты
        query = (
            select(
                Diet
            ).join(
                TrainingPlan, Diet.training_plan_id == TrainingPlan.id,
                Meal, Diet.id == Meal.diet_id,
            ).where(
                and_(
                    TrainingPlan.customer_id == customer_id,
                    TrainingPlan.start_date <= specific_day,
                    TrainingPlan.end_date >= specific_day
                )
            )
        )
        result = await uow.execute(query)
        diet = result.scalar_one_or_none()

        if diet is None:
            return None

        return DailyDietDtoSchema.from_orm(diet)
