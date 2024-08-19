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


class DietDtoSchema(BaseModel):
    """This created by coach as template"""

    id: UUID
    proteins: int
    fats: int
    carbs: int

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


class MealDtoSchema(DailyNutrients):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class DailyDietDtoSchema(DailyNutrients):
    """
    This diet fork for customer.
    This record keeps nutrition customer results.
    """

    id: UUID
    meals: list[MealDtoSchema] | None

    class Config:
        orm_mode = True
