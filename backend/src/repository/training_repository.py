from sqlalchemy import select, literal_column, insert
from sqlalchemy.orm import Session

from src import Training, ExercisesOnTraining
from src.repository.base_repository import BaseRepository


class WhooshTrainingRepository:
    async def create_training(self, db_session: Session, name, training_plan_id):
        statement = (
            insert(Training)
            .values(
                name=name,
                training_plan_id=training_plan_id,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = db_session.execute(statement).fetchone()
        if result is None:
            return None

        return training_schema.Training.from_orm(result)


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
