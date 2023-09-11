"""

"""

import uuid
from datetime import datetime

from src.domain.repositories.abstract import AbstractRepository
from src.interfaces.schemas.customer import TrainingPlanIn
from src import TrainingPlan, DietOnTrainingPlan, ExercisesOnTraining


class Nutritionist:
    """
    The subdomain of Gym to work with nutritions

    Attributes:
        diet_repo: repository to store Diet rows
        diets_on_training_repo: repository to store DietsOnTrainingPlan rows
    """

    def __init__(self, repositories: dict[str, AbstractRepository]):
        self.diet_repo = repositories["diet_repo"]
        self.diets_on_training_repo = repositories["diets_on_training_repo"]

    async def create_diets(self, training_plan_id: str, diets: list):
        """

        """
        for diet_data in diets:
            diet = await self.diet_repo.create(
                proteins=diet_data.proteins,
                fats=diet_data.fats,
                carbs=diet_data.carbs
            )

            self.diet_repo.session.add(diet)
            await self.diet_repo.session.flush()

            # bound diet with training_plan
            diet_on_training_plan = DietOnTrainingPlan(
                diet_id=str(diet.id),
                training_plan_id=training_plan_id
            )
            self.diet_repo.session.add(diet_on_training_plan)


class GymInstructor:
    """
    The subdomain of Gym to work with trainings

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


class Gym:
    """
    The service to provide fitness services for customers.

    Attributes:
        training_plan_repo: repository to store TrainingPlan rows
        gym_instructor:
        nutritionist:
    """

    def __init__(
            self,
            repositories: dict[str, AbstractRepository],
            gym_instructor: GymInstructor,
            nutritionist: Nutritionist
    ):
        self.training_plan_repo = repositories["training_plan"]
        self.gym_instructor = gym_instructor
        self.nutritionist = nutritionist

    async def create_training_plan(self, customer_id: str, data: TrainingPlanIn) -> TrainingPlan:
        """

        """
        try:
            training_plan = await self.training_plan_repo.create(
                customer_id=customer_id,
                start_date=datetime.strptime(data.start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(data.end_date, "%Y-%m-%d").date(),
                set_rest=data.set_rest,
                exercise_rest=data.exercise_rest,
                notes=data.notes
            )

            self.training_plan_repo.session.add(training_plan)
            await self.training_plan_repo.session.flush()

            await self.nutritionist.create_diets(
                training_plan_id=str(training_plan.id),
                diets=data.diets
            )
            await self.gym_instructor.create_trainings(
                training_plan_id=str(training_plan.id),
                trainings=data.trainings
            )

            await self.training_plan_repo.session.commit()
            await self.training_plan_repo.session.refresh(training_plan)

        except Exception as e:
            await self.training_plan_repo.session.rollback()
            raise

        else:
            training_plan_in_db = await self.training_plan_repo.filter(
                filters={"id": str(training_plan.id)},
                foreign_keys=["customer", "diets", "trainings"]
            )

            return training_plan_in_db[0] if training_plan_in_db else None

    async def find_training_plan(self, filters: dict) -> TrainingPlan:
        """

        """
        foreign_keys, sub_queries = ["trainings"], ["exercises"]
        training_plan = await self.training_plan_repo.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if training_plan:
            return training_plan[0]