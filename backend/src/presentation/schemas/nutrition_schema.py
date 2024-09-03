from datetime import date
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ProductOut(BaseModel):
    id: UUID
    name: str
    amount: int
    type: str
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor: str


class DailyNutrientsOut(BaseModel):
    total_calories: int
    total_proteins: int
    total_fats: int
    total_carbs: int

    consumed_calories: int
    consumed_proteins: int
    consumed_fats: int
    consumed_carbs: int


class DailyMealsOut(BaseModel):
    date: date
    daily_total: DailyNutrientsOut
    breakfast: dict
    lunch: dict
    dinner: dict
    snacks: dict

    @classmethod
    def from_diet_dto(cls, diet_dto: "DailyDietDtoSchema") -> "DailyMealsOut":
        daily_total = DailyNutrientsOut(
            total_calories=diet_dto.total_calories,
            total_proteins=diet_dto.total_proteins,
            total_fats=diet_dto.total_fats,
            total_carbs=diet_dto.total_carbs,
            consumed_calories=diet_dto.consumed_calories,
            consumed_proteins=diet_dto.consumed_proteins,
            consumed_fats=diet_dto.consumed_fats,
            consumed_carbs=diet_dto.consumed_carbs,
        )

        return DailyMealsOut(
            date=diet_dto.date,
            daily_total=daily_total,
            breakfast=diet_dto.breakfast,
            lunch=diet_dto.lunch,
            dinner=diet_dto.dinner,
            snacks=diet_dto.snacks,
        )


class DailyMealOut(BaseModel):
    total: DailyNutrientsOut
    products: list[ProductOut]


@dataclass
class DailyDietOut:
    date: str
    actual_nutrition: DailyMealsOut | None


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACKS = "snacks"


class ProductAddInDiet(BaseModel):
    barcode: str
    amount: int


class ProductToDietRequest(BaseModel):
    diet_id: UUID
    meal_type: MealType
    specific_day: str
    product_data: list[ProductAddInDiet]
