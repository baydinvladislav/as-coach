from pydantic import BaseModel

from src.persistence.dynamo_db_models import Product


class ProductDtoSchema(BaseModel):
    barcode: str
    name: str
    type: str
    proteins: int
    fats: int
    carbs: int
    calories: int
    vendor_name: str
    user_id: str

    @classmethod
    def from_product(cls, product_db_row: Product) -> "ProductDtoSchema":
        return cls(
            barcode=product_db_row.barcode,
            name=product_db_row.name,
            type=product_db_row.type,
            proteins=product_db_row.proteins,
            fats=product_db_row.fats,
            carbs=product_db_row.carbs,
            calories=product_db_row.calories,
            vendor_name=product_db_row.vendor_name,
            user_id=product_db_row.user_id,
        )
