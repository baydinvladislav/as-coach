from uuid import UUID

from src.presentation.schemas.product_schema import ProductCreateIn
from src.repository.product_repository import ProductRepository
from src.schemas.product_dto import ProductDtoSchema


class CaloriesCalculatorService:
    @staticmethod
    async def calculate_calories(proteins: int, fats: int, carbs: int) -> int:
        protein_coefficient = 4
        carb_coefficient = 4
        fat_coefficient = 9
        result = (proteins * protein_coefficient) + (carbs * carb_coefficient) + (fats * fat_coefficient)
        return result


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        calories_calculator_service: CaloriesCalculatorService,
    ) -> None:
        self.product_repository = product_repository
        self.calories_calculator_service = calories_calculator_service

    async def get_product_by_id(self, _id: UUID) -> ProductDtoSchema:
        ...

    async def get_products_by_ids(self, product_ids: list[UUID]) -> list[ProductDtoSchema]:
        ...

    async def create_product(self, user_id: UUID, product_data: ProductCreateIn) -> ProductDtoSchema:
        product_calories = await self.calories_calculator_service.calculate_calories(
            proteins=product_data.proteins,
            fats=product_data.fats,
            carbs=product_data.carbs,
        )
        new_product = await self.product_repository.insert_product(
            user_id,
            product_data,
            product_calories,
        )
        return ProductDtoSchema.from_product(new_product)
