from uuid import UUID, uuid4

from src.persistence.dynamo_db_models import Product
from src.presentation.schemas.product_schema import ProductCreateIn


class ProductRepository:
    async def insert_product(self, user_id: UUID, product_data: ProductCreateIn, product_calories: int) -> Product:
        new_product = Product(
            id=str(uuid4()),
            name=product_data.name,
            barcode=product_data.barcode,
            product_type=product_data.product_type,
            proteins=product_data.proteins,
            fats=product_data.fats,
            carbs=product_data.carbs,
            calories=product_calories,
            vendor_name=product_data.vendor_name,
            user_id=str(user_id),
        )
        new_product.save()
        return new_product
