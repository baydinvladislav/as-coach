from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src import Exercise, MuscleGroup
from src.schemas.muscle_group_dto import MuscleGroupDto


class ExerciseSchemaDto(BaseModel):
    id: UUID
    name: str


class ExerciseRepository:
    async def get_coach_exercises(self, uow: AsyncSession, coach_id: str) -> list[ExerciseSchemaDto]:
        query = (
            select(Exercise)
            .where(
                or_(Exercise.coach_id.is_(None), Exercise.coach_id == UUID(coach_id))
            )
        )
        result = await uow.execute(query)
        exercises = result.fetchall()
        return [ExerciseSchemaDto.from_orm(exercise) for exercise in exercises]


class MuscleGroupRepository:
    async def get_specified_muscle_group(self, uow: AsyncSession, muscle_group_id: str) -> MuscleGroupDto | None:
        query = (
            select(MuscleGroup).where(MuscleGroup.id == UUID(muscle_group_id))
        )
        result = await uow.execute(query)
        muscle_group = result.scalar_one_or_none()

        if muscle_group is None:
            return None

        return MuscleGroupDto.from_orm(muscle_group)

    async def get_all_muscle_groups(self, uow: AsyncSession) -> list[MuscleGroupDto]:
        query = select(MuscleGroup)
        result = await uow.execute(query)
        muscle_groups = result.fetchall()
        return [MuscleGroupDto.from_orm(muscle_group) for muscle_group in muscle_groups]
