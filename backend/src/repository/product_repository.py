from uuid import UUID, uuid4

from src.persistence.dynamo_db_models import Product
from src.presentation.schemas.product_schema import ProductCreateIn
from src.schemas.product_dto import ProductDtoSchema


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

    async def delete_product(self, _id: str) -> str | None:
        ...

    async def update_product(self, _id: str) -> ProductDtoSchema | None:
        ...

    async def search_product(self, query_text: str) -> ProductDtoSchema | None:
        ...
