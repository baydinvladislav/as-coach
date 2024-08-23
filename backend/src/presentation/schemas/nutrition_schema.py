from dataclasses import dataclass
from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src.schemas.diet_dto import DailyDietDtoSchema


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

    class Config:
        orm_mode = True


class DailyNutrientsOut(BaseModel):
    calories_total: int
    calories_consumed: int

    proteins_total: int
    proteins_consumed: int

    fats_total: int
    fats_consumed: int

    carbs_total: int
    carbs_consumed: int


class DailyMealsOut(BaseModel):
    daily_total: DailyNutrientsOut
    breakfast: dict
    lunch: dict
    dinner: dict
    snacks: dict

    @classmethod
    def from_diet_dto(cls, diet_dto: DailyDietDtoSchema) -> "DailyMealsOut":
        daily_total = DailyNutrientsOut(
            calories_total=diet_dto.total_calories,
            calories_consumed=diet_dto.consumed_calories,
            proteins_total=diet_dto.total_proteins,
            proteins_consumed=diet_dto.consumed_proteins,
            fats_total=diet_dto.total_fats,
            fats_consumed=diet_dto.consumed_fats,
            carbs_total=diet_dto.total_carbs,
            carbs_consumed=diet_dto.consumed_carbs,
        )

        return DailyMealsOut(
            daily_total=daily_total,
            breakfast=diet_dto.breakfast,
            lunch=diet_dto.lunch,
            dinner=diet_dto.dinner,
            snacks=diet_dto.snacks,
        )

    class Config:
        orm_mode = True


@dataclass
class DailyDietOut:
    date: date
    actual_nutrition: DailyMealsOut
