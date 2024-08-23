from uuid import UUID

from pydantic import BaseModel


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
    consumed_proteins: int

    total_fats: int
    consumed_fats: int

    total_carbs: int
    consumed_carbs: int

    total_calories: int
    consumed_calories: int

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
    consumed_calories: int

    total_proteins: int
    consumed_proteins: int

    total_fats: int
    consumed_fats: int

    total_carbs: int
    consumed_carbs: int

    breakfast: dict
    lunch: dict
    dinner: dict
    snacks: dict

    class Config:
        orm_mode = True
