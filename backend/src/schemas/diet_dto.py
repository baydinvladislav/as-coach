from uuid import UUID
from datetime import date

from pydantic import BaseModel

from src import Diet


class ProductDtoSchema(BaseModel):
    id: UUID
    name: str
    amount: int
    type: str
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor_name: str

    class Config:
        orm_mode = True


class DietDtoSchema(BaseModel):
    """This created by coach as template"""

    id: UUID
    total_proteins: int
    total_fats: int
    total_carbs: int
    total_calories: int

    class Config:
        orm_mode = True


class DailyNutrients(BaseModel):
    """
    Nutrition plan/fact model.
    Inherited by Meal and DailyDiet.
    """

    total_calories: int
    consumed_calories: int

    total_proteins: int
    consumed_proteins: int

    total_fats: int
    consumed_fats: int

    total_carbs: int
    consumed_carbs: int

    class Config:
        orm_mode = True


class DailyDietDtoSchema(BaseModel):
    """
    This diet fork for customer.
    This record keeps nutrition customer results.
    """

    id: UUID

    total_calories: int
    total_proteins: int
    total_fats: int
    total_carbs: int

    breakfast: dict
    lunch: dict
    dinner: dict
    snacks: dict

    @classmethod
    def from_diet(cls, template_diet: Diet, specific_day: date) -> "DailyDietDtoSchema":
        customer_fact_days = template_diet.diet_days

        if customer_fact_days is None:
            # клиент не списал ни одного дня с диеты
            ...

        specific_day_fact = next((day for day in customer_fact_days if day.date == specific_day), None)

        if specific_day_fact is None:
            # клиент не списал запрашиваемый день
            ...

        return DailyDietDtoSchema(
            # recommend amount by coach
            total_calories=template_diet.total_calories,
            total_proteins=template_diet.total_proteins,
            total_fats=template_diet.total_fats,
            total_carbs=template_diet.total_carbs,

            # fact amount
            id=specific_day_fact.id,

            breakfast=specific_day_fact.breakfast,
            lunch=specific_day_fact.lunch,
            dinner=specific_day_fact.dinner,
            snacks=specific_day_fact.snacks,
        )

    class Config:
        orm_mode = True
