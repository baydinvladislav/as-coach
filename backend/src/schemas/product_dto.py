from uuid import UUID

from pydantic import BaseModel

from src.persistence.dynamo_db_models import Product


class ProductDtoSchema(BaseModel):
    id: UUID
    name: str
    barcode: str
    product_type: str
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor_name: str
    user_id: UUID

    @classmethod
    def from_product(cls, product_db_row: Product) -> "ProductDtoSchema":
        return cls(
            id=product_db_row.id,
            name=product_db_row.name,
            barcode=product_db_row.barcode,
            product_type=product_db_row.product_type,
            proteins=product_db_row.proteins,
            fats=product_db_row.fats,
            carbs=product_db_row.carbs,
            calories=product_db_row.calories,
            vendor_name=product_db_row.vendor_name,
            user_id=product_db_row.user_id,
        )
