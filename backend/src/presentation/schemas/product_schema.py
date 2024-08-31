from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    vendor_name: str
    barcode: str
    type: str
    portion_size: int | None
    proteins: int
    fats: int
    carbs: int


class ProductCreateIn(ProductBase):
    pass


class ProductCreateOut(ProductBase):
    id: str
    calories: int
    user_id: str
