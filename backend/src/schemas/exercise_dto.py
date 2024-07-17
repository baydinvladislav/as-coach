from uuid import UUID

from pydantic import BaseModel


class ExerciseDtoSchema(BaseModel):
    id: UUID
    name: str
    coach_id: UUID | None
    # где-то в коде нужно, а где-то нет
    muscle_group_id: UUID | None
    muscle_group_name: str | None

    class Config:
        orm_mode = True
