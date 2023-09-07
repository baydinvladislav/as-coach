"""

"""

import uuid
from datetime import datetime

from src.core.repositories.abstract import AbstractRepository
from src.core.repositories.repos import DietRepository, TrainingRepository, DietOnTrainingPlanRepository
from src.infrastructure.schemas.customer import TrainingPlanIn
from src.gym.models import DietOnTrainingPlan, ExercisesOnTraining


# class DietOnTrainingPlanService:
#     def __init__(self, diet_on_training_repo: AbstractRepository):
#         self.diet_on_training_repo = diet_on_training_repo
#
#     async def create_diets_in_training_plan(self, training_plan_id: str, diet_id: str):
#         # bound diet with training_plan
#         diet_on_training_plan = DietOnTrainingPlan(
#             diet_id=diet_id,
#             training_plan_id=training_plan_id
#         )
#         self.diet_on_training_repo.session.add(diet_on_training_plan)


class DietService:
    """

    """

    def __init__(self, diet_repo: AbstractRepository):
        self.diet_repo = diet_repo

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


class TrainingService:
    """

    """

    def __init__(self, training_repo: AbstractRepository):
        self.training_repo = training_repo
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


class TrainingPlanService:
    """

    """

    def __init__(self, training_plan_repo: AbstractRepository):
        self.training_plan_repo = training_plan_repo

        self.diet_service = DietService(DietRepository(training_plan_repo.session))
        self.training_service = TrainingService(TrainingRepository(training_plan_repo.session))

    async def create(self, customer_id: str, data: TrainingPlanIn):
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

            await self.diet_service.create_diets(
                training_plan_id=str(training_plan.id),
                diets=data.diets
            )
            await self.training_service.create_trainings(
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
