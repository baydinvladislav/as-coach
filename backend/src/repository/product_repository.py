from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src import CustomerHistoryProducts
from src.persistence.dynamo_db_models import Product
from src.presentation.schemas.product_schema import ProductCreateIn
from src.schemas.product_dto import ProductDtoSchema, HistoryProductDtoSchema


class ProductRepository:
    async def get_product_by_barcode(self, barcode: str) -> ProductDtoSchema | None:
        try:
            product = Product.get(barcode)
        except Product.DoesNotExist:
            return None
        return ProductDtoSchema.from_product(product)

    async def get_products_by_barcodes(self, barcodes: list[str]) -> list[ProductDtoSchema]:
        products = []
        for product in Product.batch_get(barcodes):
            if product:
                products.append(ProductDtoSchema.from_product(product))
        return products

    async def insert_product(
        self,
        user_id: UUID,
        product_data: ProductCreateIn,
        product_calories: int
    ) -> ProductDtoSchema:
        new_product = Product(
            barcode=product_data.barcode,
            name=product_data.name,
            type=product_data.type,
            proteins=product_data.proteins,
            fats=product_data.fats,
            carbs=product_data.carbs,
            calories=product_calories,
            vendor_name=product_data.vendor_name,
            user_id=str(user_id),
        )
        new_product.save()
        return ProductDtoSchema.from_product(new_product)

    async def insert_products_to_history(
        self,
        uow: AsyncSession,
        product_list: list[dict],
    ) -> None:
        products_history_orm = [
            CustomerHistoryProducts(
                name=product["name"],
                type=product["type"],
                proteins=product["proteins"],
                fats=product["fats"],
                carbs=product["carbs"],
                calories=product["calories"],
                vendor_name=product["vendor_name"],
                customer_id=product["user_id"],
                barcode=product["barcode"],
                amount=product["amount"],
            ) for product in product_list
        ]
        uow.add_all(products_history_orm)

    async def fetch_product_history(self, uow: AsyncSession, customer_id: UUID) -> list[HistoryProductDtoSchema]:
        query = (
            select(
                CustomerHistoryProducts
            )
            .where(CustomerHistoryProducts.customer_id == customer_id)
            .order_by(desc(CustomerHistoryProducts.created))
            .limit(20)
        )

        result = await uow.execute(query)
        product_history = result.scalars().all()

        product_history_dto = [
            HistoryProductDtoSchema(
                name=ph.name,
                type=ph.type,
                proteins=ph.proteins,
                fats=ph.fats,
                carbs=ph.carbs,
                calories=ph.calories,
                vendor_name=ph.vendor_name,
                customer_id=str(ph.customer_id),
                barcode=ph.barcode,
                amount=ph.amount,
            )
            for ph in product_history
        ]
        return product_history_dto

    async def lookup_products(self, query_text: str) -> list[ProductDtoSchema]:
        condition = (Product.name.contains(query_text)) | (Product.vendor_name.contains(query_text))
        scan_results = Product.scan(condition)
        products = [
            ProductDtoSchema.from_product(product)
            for product in scan_results
        ]
        return products

    async def delete_product(self, _id: str) -> str | None:
        ...

    async def update_product(self, _id: str) -> ProductDtoSchema | None:
        ...
