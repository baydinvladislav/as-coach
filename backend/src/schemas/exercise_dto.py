from uuid import UUID

from pydantic import BaseModel


class ExerciseDtoSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
