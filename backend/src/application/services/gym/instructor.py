import uuid

from src import ExercisesOnTraining
from src.domain.repositories.abstract import AbstractRepository


class Instructor:
    """
    The service responsible for trainings operations

    Attributes:
        training_repo: repository to store Training rows
        exercises_on_training_repo: repository to store ExercisesOnTraining rows
        superset_dict: using to store supersets
        ordering: make order for supersets
    """

    def __init__(self, repositories: dict[str, AbstractRepository]):
        self.training_repo = repositories["training_repo"]
        self.exercises_on_training_repo = repositories["exercises_on_training_repo"]
        self.superset_dict = {}
        self.ordering = 0

    async def update_superset_dict(self, exercise_item):
        """

        """
        if isinstance(exercise_item.supersets, list) and len(exercise_item.supersets) > 0:
            if str(exercise_item.id) not in self.superset_dict:
                superset_id = str(uuid.uuid4())

                self.superset_dict[str(exercise_item.id)] = superset_id
                for e in exercise_item.supersets:
                    self.superset_dict[str(e)] = superset_id

    async def create_trainings(self, training_plan_id: str, trainings: list):
        """
        Creates trainings in customer training plan

        Args:
            training_plan_id: UUID of training plan
            trainings: data for creating trainings
        """
        for training_item in trainings:
            training = await self.training_repo.create(
                name=training_item.name,
                training_plan_id=training_plan_id
            )

            self.training_repo.session.add(training)
            await self.training_repo.session.flush()

            self.superset_dict = {}
            self.ordering = 0
            for exercise_item in training_item.exercises:
                await self.update_superset_dict(exercise_item)

                exercise_on_training = ExercisesOnTraining(
                    training_id=str(training.id),
                    exercise_id=str(exercise_item.id),
                    sets=exercise_item.sets,
                    superset_id=self.superset_dict.get(str(exercise_item.id)),
                    ordering=self.ordering
                )
                self.training_repo.session.add(exercise_on_training)
                await self.training_repo.session.flush()
                self.ordering += 1

    async def provide_training_exercises(self, training_id, exercise_id):
        return await self.exercises_on_training_service.get_exercises_on_training(
            training_id=training_id,
            exercise_id=exercise_id
        )

    async def get_training_exercises(self, training_id, exercise_id):
        await self.training_service.provide_training_exercises(
            training_id=training_id,
            exercise_id=exercise_id
        )
