from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src import Exercise, MuscleGroup


class ExerciseRepository:
    async def filter(self, uow: AsyncSession, coach_id: UUID):
        query = (
            select(Exercise)
            .where(
                or_(Exercise.coach_id.is_(None), Exercise.coach_id == coach_id)
            )
            .options(selectinload(Exercise.muscle_group))
        )

        result = await uow.execute(query)
        exercises = result.scalars().all()
        return exercises


class MuscleGroupRepository:
    ...
