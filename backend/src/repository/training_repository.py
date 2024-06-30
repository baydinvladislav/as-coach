from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import Training, ExercisesOnTraining
from src.repository.base_repository import BaseRepository
from src.schemas.training_dto import ScheduleExercisesDtoSchema


class TrainingRepository:
    def __init__(self) -> None:
        self.superset_dict = {}
        self.ordering = 0

    async def provide_schedule_exercises_by_training_id(self, uow: AsyncSession, training_id: str):
        query = select(Training).where(Training.id == training_id)
        result = await uow.execute(query)
        schedule_exercises = result.scalars().first()
        return [ScheduleExercisesDtoSchema.from_orm(st) for st in schedule_exercises]

    async def _update_superset_dict(self, exercise_item):
        if isinstance(exercise_item.supersets, list) and len(exercise_item.supersets) > 0:
            if str(exercise_item.id) not in self.superset_dict:
                superset_id = str(uuid4())

                self.superset_dict[str(exercise_item.id)] = superset_id
                for e in exercise_item.supersets:
                    self.superset_dict[str(e)] = superset_id

    async def create_trainings(self, uow: AsyncSession, training_plan_id: UUID, trainings: list):
        new_trainings = [
            Training(name=training_item.name, training_plan_id=training_plan_id) for training_item in trainings
        ]

        uow.add_all(new_trainings)
        await uow.flush()

        exercises_on_training = []
        for training, training_item in zip(new_trainings, trainings):
            self.superset_dict = {}
            self.ordering = 0
            for exercise_item in training_item.exercises:
                await self._update_superset_dict(exercise_item)
                exercises_on_training.append(ExercisesOnTraining(
                    training_id=str(training.id),
                    exercise_id=str(exercise_item.id),
                    sets=exercise_item.sets,
                    superset_id=self.superset_dict.get(str(exercise_item.id)),
                    ordering=self.ordering
                ))
                self.ordering += 1

        uow.add_all(exercises_on_training)
        await uow.flush()


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
