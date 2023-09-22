from src.domains.repositories.abstract import AbstractRepository


class Library:
    """
    The service to organize data in gym library
    """

    def __init__(
            self,
            repositories: dict[str, AbstractRepository]
    ):
        self.exercise_repo = repositories["exercise"]
        self.muscle_group_repo = repositories["muscle_group"]

    async def get_exercise_list(self, coach_id: str):
        """
        Provides list of default exercises plus custom coach exercises

        Args:
            coach_id: coach UUID
        """
        exercises = await self.exercise_repo.filter({"coach_id": coach_id})
        return exercises

    async def get_muscle_group_list(self):
        """
        Provides available muscle groups
        """
        muscle_groups = await self.muscle_group_repo.get_all()
        return muscle_groups

    async def create_exercise(self, exercise_name: str, coach_id: str, muscle_group_id: str):
        """
        Provides available muscle groups

        Args:
            exercise_name: passed name of exercise
            coach_id: coach UUID
            muscle_group_id: muscle group UUID
        """
        muscle_group = await self.muscle_group_repo.get(muscle_group_id)

        if not muscle_group:
            raise

        exercise = await self.exercise_repo.create(
            name=exercise_name,
            coach_id=coach_id,
            muscle_group=muscle_group
        )

        return exercise
