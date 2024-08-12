from uuid import UUID

from pydantic import BaseModel


# нужно как-то определять потребленные и текущие
# добавить приёмы пищи
class DietDtoSchema(BaseModel):
    id: UUID
    proteins: int
    fats: int
    carbs: int

    class Config:
        orm_mode = True


class Product:
    id: UUID
    name: str
    amount: int
    type: str  # enum
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor: str  # class Vendor(BaseSQLAlchemy):


class Meal:
    name: str  # literal: breakfast, lunch, dinner, snacks
    total: int
    products: list[Product]


class DailyDietDtoSchema(DietDtoSchema):
    total_nutrients: int

    consumed_proteins: int
    consumed_fats: int
    consumed_carbs: int

    total_calories: int
    consumed_calories: int

    meals: list[Meal]
