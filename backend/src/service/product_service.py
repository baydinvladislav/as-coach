from uuid import UUID

from src.presentation.schemas.product_schema import ProductCreateIn
from src.repository.product_repository import ProductRepository
from src.schemas.product_dto import ProductDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        calories_calculator_service: CaloriesCalculatorService,
    ) -> None:
        self.product_repository = product_repository
        self.calories_calculator_service = calories_calculator_service

    async def get_product_by_id(self, _id: UUID) -> ProductDtoSchema | None:
        product = await self.product_repository.get_product_by_id(str(_id))
        return product

    async def get_products_by_ids(self, product_ids: list[str]) -> list[ProductDtoSchema]:
        products = await self.product_repository.get_products_by_ids(product_ids)
        return products

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
        return new_product
