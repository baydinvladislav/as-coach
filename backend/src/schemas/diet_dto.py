from uuid import UUID

from pydantic import BaseModel


class DietDtoSchema(BaseModel):
    id: UUID
    proteins: int
    fats: int
    carbs: int

    class Config:
        orm_mode = True
