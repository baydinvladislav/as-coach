from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import Training, ExercisesOnTraining
from src.repository.base_repository import BaseRepository
from src.schemas.training_dto import ScheduleExercisesDtoSchema


class TrainingRepository:
    async def provide_schedule_exercises_by_training_id(self, uow: AsyncSession, training_id: str):
        query = select(Training).where(Training.id == training_id)
        result = await uow.execute(query)
        schedule_exercises = result.scalars().first()
        return [ScheduleExercisesDtoSchema.from_orm(st) for st in schedule_exercises]


class ExercisesOnTrainingRepository(BaseRepository):
    model = ExercisesOnTraining

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        result = await self.session.execute(
            select(self.model).order_by(self.model.ordering).where(
                self.model.training_id.in_(filters["training_ids"])
            )
        )

        instances = result.scalars().all()
        return instances
