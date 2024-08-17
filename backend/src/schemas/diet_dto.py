from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
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


class DailyNutrients(BaseModel):
    total_calories: int
    consumed_calories: int

    total_proteins: int
    consumed_proteins: int

    total_fats: int
    consumed_fats: int

    total_carbs: int
    consumed_carbs: int


class MealDtoSchema(DailyNutrients):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class DailyDietDtoSchema(DailyNutrients):
    id: UUID
    meals: list[MealDtoSchema]

    class Config:
        orm_mode = True
