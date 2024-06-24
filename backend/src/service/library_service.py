from src.repository.library_repository import ExerciseRepository, MuscleGroupRepository


class LibraryService:
    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        muscle_group_repository: MuscleGroupRepository
    ) -> None:
        self.exercise_repository = exercise_repository
        self.muscle_group_repository = muscle_group_repository

    async def get_exercise_list(self, coach_id: str):
        exercises = await self.exercise_repository.filter({"coach_id": coach_id})
        return exercises

    async def get_muscle_group_list(self):
        muscle_groups = await self.muscle_group_repository.get_all()
        return muscle_groups

    async def create_exercise(self, exercise_name: str, coach_id: str, muscle_group_id: str):
        muscle_group = await self.muscle_group_repository.get(muscle_group_id)

        if not muscle_group:
            raise

        exercise = await self.exercise_repository.create(
            name=exercise_name,
            coach_id=coach_id,
            muscle_group=muscle_group
        )

        return exercise
