from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from src import Exercise, MuscleGroup
from src.repository.base_repository import BaseRepository


class ExerciseRepository(BaseRepository):
    model = Exercise

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        query = select(Exercise).where(
            or_(Exercise.coach_id.is_(None), Exercise.coach_id == filters["coach_id"])
        ).options(selectinload(Exercise.muscle_group))

        result = await self.session.execute(query)
        exercises = result.scalars().all()
        return exercises


class MuscleGroupRepository(BaseRepository):
    model = MuscleGroup
