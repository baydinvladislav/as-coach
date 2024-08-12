from datetime import date
from uuid import UUID

from src.schemas.diet_dto import DietDtoSchema


class ProductOut:
    id: UUID
    name: str
    amount: int
    type: str
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor: str


class DailyNutrientsOut:
    calories_total: int
    calories_consumed: int

    proteins_total: int
    fats_total: int
    carbs_total: int

    proteins_consumed: int
    fats_consumed: int
    carbs_consumed: int


class DailyMealOut:
    nutrients: list[DailyNutrientsOut]
    products: ProductOut


class DailyDietOut:
    daily_total: DailyNutrientsOut
    breakfast: DailyMealOut
    lunch: DailyMealOut
    dinner: DailyMealOut
    snacks: DailyMealOut

    def from_daily_diet_dto(cls, daily_diet_dto: DietDtoSchema) -> "DailyDietOut":
        return DailyDietOut(

        )


class DailyNutritionOut:
    date: date
    actual_nutrition: DailyDietOut
