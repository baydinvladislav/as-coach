from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    barcode: str
    product_type: str
    proteins: int
    fats: int
    carbs: int
    vendor_name: str


class ProductCreateIn(ProductBase):
    pass


class ProductCreateOut(ProductBase):
    id: str
    calories: int
    user_id: str
