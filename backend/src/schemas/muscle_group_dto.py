from uuid import UUID

from pydantic import BaseModel


class MuscleGroupDto(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
