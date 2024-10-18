from pydantic import BaseModel, validator


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

    @classmethod
    @validator("name", "vendor_name", pre=True)
    def check_lowercase(cls, v: str) -> str:
        return v.lower()


class ProductCreateOut(ProductBase):
    calories: int
    user_id: str

    @classmethod
    @validator("name", "vendor_name", pre=True)
    def check_lowercase(cls, v: str) -> str:
        return v.capitalize()
