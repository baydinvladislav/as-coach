import uuid

from src import ExercisesOnTraining
from src.repository.training_repository import TrainingRepository, ExercisesOnTrainingRepository


class TrainingService:
    """
    The service responsible for trainings operations

    Attributes:
        training_repository: repository to store Training rows
        exercises_on_training_repository: repository to store ExercisesOnTraining rows
        superset_dict: using to store supersets
        ordering: make order for supersets
    """

    def __init__(
        self,
        uow_ro_factory: UnitOfWorkFactory,
        uow_write_factory: UnitOfWorkFactory,
        training_repository: TrainingRepository,
        exercises_on_training_repository: ExercisesOnTrainingRepository,
    ) -> None:
        self.uow_ro_factory = uow_ro_factory
        self.uow_write_factory = uow_write_factory
        self.training_repository = training_repository
        self.exercises_on_training_repository = exercises_on_training_repository
        self.superset_dict = {}
        self.ordering = 0

    async def _create_trainings(self, training_plan_id: str, trainings: list):
        ...

    async def update_superset_dict(self, exercise_item):
        """
        Implement superset creations for set of trainings

        Args:
            exercise_item: secondary table object between training and exercise
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
            training = await self.training_repository.create(
                name=training_item.name,
                training_plan_id=training_plan_id
            )

            self.training_repository.session.add(training)
            await self.training_repository.session.flush()

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
                self.training_repository.session.add(exercise_on_training)
                await self.training_repository.session.flush()
                self.ordering += 1

    async def provide_scheduled_trainings(self, training_ids: list, exercise_ids: list) -> dict:
        """
        Provides scheduled training for training plan

        Args:
            training_ids: specified trainings
            exercise_ids: specified exercises

        Returns:
            all scheduled training for training plan
        """
        exercises = await self.exercises_on_training_repository.filter({
            "training_ids": training_ids,
            "exercise_ids": exercise_ids
        })

        scheduled_trainings = dict()
        for exercise in exercises:
            scheduled_trainings[str(exercise.exercise_id)] = exercise

        return scheduled_trainings
