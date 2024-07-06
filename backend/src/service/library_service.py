from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.library_repository import ExerciseRepository, MuscleGroupRepository
from src.schemas.muscle_group_dto import MuscleGroupDto


class LibraryService:
    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        muscle_group_repository: MuscleGroupRepository
    ) -> None:
        self.exercise_repository = exercise_repository
        self.muscle_group_repository = muscle_group_repository

    async def get_exercise_list(self, uow: AsyncSession, coach_id: str):
        exercises = await self.exercise_repository.get_coach_exercises(uow, coach_id)
        return exercises

    async def get_muscle_group_list(self, uow: AsyncSession) -> list[MuscleGroupDto]:
        muscle_groups = await self.muscle_group_repository.get_all_muscle_groups(uow)
        return muscle_groups

    async def create_exercise(self, uow: AsyncSession, exercise_name: str, coach_id: str, muscle_group_id: str):
        muscle_group = await self.muscle_group_repository.get_specified_muscle_group(uow, muscle_group_id)

        if not muscle_group:
            raise

        exercise = await self.exercise_repository.create(
            name=exercise_name,
            coach_id=coach_id,
            muscle_group=muscle_group
        )

        return exercise
