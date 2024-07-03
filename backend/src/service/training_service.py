from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.training_repository import TrainingRepository


class TrainingService:
    def __init__(self, training_repository: TrainingRepository):
        self.training_repository = training_repository

    async def create_trainings(self, uow: AsyncSession, training_plan_id: UUID, trainings: list) -> int:
        inserted_rows = await self.training_repository.create_personal_trainings(uow, training_plan_id, trainings)
        return inserted_rows

    async def provide_scheduled_trainings(self, uow: AsyncSession, training_ids: list) -> dict:
        exercises = await self.training_repository.provide_schedule_exercises_by_training_id(
            uow=uow,
            training_id=training_ids,
        )

        scheduled_trainings = dict()
        for exercise in exercises:
            scheduled_trainings[str(exercise.exercise_id)] = exercise

        return scheduled_trainings
