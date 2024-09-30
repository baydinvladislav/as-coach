from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.product_schema import ProductCreateIn
from src.repository.product_repository import ProductRepository
from src.shared.exceptions import BarcodeAlreadyExistExc
from src.schemas.product_dto import ProductDtoSchema, HistoryProductDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        calories_calculator_service: CaloriesCalculatorService,
    ) -> None:
        self.product_repository = product_repository
        self.calories_calculator_service = calories_calculator_service

    async def get_product_by_barcode(self, barcode: str) -> ProductDtoSchema | None:
        product = await self.product_repository.get_product_by_barcode(barcode)
        return product

    async def get_products_by_barcodes(self, barcodes: list[str]) -> list[ProductDtoSchema]:
        products = await self.product_repository.get_products_by_barcodes(barcodes)
        return products

    async def create_product(self, uow: AsyncSession, user_id: UUID, product_data: ProductCreateIn) -> ProductDtoSchema:
        existed_product = await self.get_product_by_barcode(product_data.barcode)
        if existed_product is not None:
            raise BarcodeAlreadyExistExc("The product with the same barcode already exist")

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
        await uow.commit()
        return new_product

    async def save_product_to_history(self, uow: AsyncSession, product_list: list[dict]) -> None:
        await self.product_repository.insert_products_to_history(uow, product_list)

    async def get_product_history(self, uow: AsyncSession, customer_id: UUID) -> list[HistoryProductDtoSchema]:
        return await self.product_repository.fetch_product_history(uow, customer_id)
