from sqlalchemy import select

from src import Training, ExercisesOnTraining
from src.repository.base import BaseRepository


class TrainingRepository(BaseRepository):
    model = Training


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
