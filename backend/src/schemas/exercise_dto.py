from uuid import UUID

from pydantic import BaseModel


class ExerciseDtoSchema(BaseModel):
    id: UUID
    name: str
    coach_id: UUID | None
    muscle_group_name: str
    muscle_group_id: UUID

    class Config:
        orm_mode = True
