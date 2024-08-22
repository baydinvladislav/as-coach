from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src import Meal


class MealRepository:
    async def insert_empty_meals(self, uow: AsyncSession, diets: list[UUID]) -> int:
        default_meals = ["breakfast", "lunch", "dinner", "snacks"]

        for default_meal in default_meals:
            meals_orm = [
                Meal(
                    name=default_meal,
                    diet=diet,
                    total_calories=diet.calories,
                    total_proteins=diet.proteins,
                    total_fats=diet.fats,
                    total_carbs=diet.carbs,
                )
                for diet in diets
            ]

        uow.add_all(meals_orm)
        await uow.flush()

        meals = [meal.id for meal in meals_orm]
        return len(meals)
