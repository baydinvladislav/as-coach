from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.training_repository import TrainingRepository
from src.schemas.exercise_dto import ScheduledExerciseDto


class TrainingService:
    def __init__(self, training_repository: TrainingRepository):
        self.training_repository = training_repository

    async def create_trainings(self, uow: AsyncSession, training_plan_id: UUID, trainings: list) -> int:
        inserted_rows = await self.training_repository.create_personal_trainings(
            uow=uow,
            training_plan_id=training_plan_id,
            customer_trainings=trainings,
        )
        return inserted_rows

    async def provide_scheduled_trainings(
        self,
        uow: AsyncSession,
        training_ids: list[str],
        exercise_ids: list[str]
    ) -> dict[str, ScheduledExerciseDto]:
        scheduled_trainings = await self.training_repository.provide_schedule_exercises_by_training_id(
            uow=uow,
            training_ids=training_ids,
            exercise_ids=exercise_ids,
        )

        result = dict()
        for exercise in scheduled_trainings:
            result[str(exercise.exercise_id)] = exercise

        return result
