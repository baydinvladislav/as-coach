"""
Contains services related to the Gym functionality
"""

from datetime import datetime
from dataclasses import dataclass

from src.service.abstract import TrainingManagerInterface
from src.service.training import TrainingService
from src.service.diet import DietService
from src.repository.abstract import AbstractRepository
from src.schemas.customer import TrainingPlanIn
from src import TrainingPlan


# @dataclass
# class TrainingPlanService:
#     """
#     The service to provide fitness services for customers.
#
#     Attributes:
#         training_plan_repository: repository to store TrainingPlan rows
#         training_plan_repository: the service responsible for diets operations
#         training_service: the service responsible for trainings operations
#     """
#     training_plan_repository: TrainingPlanRepository
#     diet_service: DietService
#     training_service: TrainingService
#
#     async def create_training_plan(self, customer_id: str, data: TrainingPlanIn) -> TrainingPlan:
#         ...
#
#     async def find_training_plan(self, filters: dict) -> dict:
#         ...


class TrainingPlanService(TrainingManagerInterface):
    """
    The service to provide fitness services for customers.

    Attributes:
        training_plan_repository: repository to store TrainingPlan rows
        training_service: the service responsible for trainings operations
        diet_service: the service responsible for diets operations
    """

    def __init__(
            self,
            repositories: dict[str, AbstractRepository],
            training_service: TrainingService,
            diet_service: DietService
    ):
        self.training_plan_repository = repositories["training_plan"]
        self.training_service = training_service
        self.diet_service = diet_service

    async def create_training_plan(self, customer_id: str, data: TrainingPlanIn) -> TrainingPlan:
        """
        Creates training plan for customer

        Args:
            customer_id: UUID of the customer for whom the training plan is being created
            data: data from client for creating new training plan
        """
        try:
            training_plan = await self.training_plan_repository.create(
                customer_id=customer_id,
                start_date=datetime.strptime(data.start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(data.end_date, "%Y-%m-%d").date(),
                set_rest=data.set_rest,
                exercise_rest=data.exercise_rest,
                notes=data.notes
            )

            self.training_plan_repository.session.add(training_plan)
            await self.training_plan_repository.session.flush()

            await self.diet_service.create_diets(
                training_plan_id=str(training_plan.id),
                diets=data.diets
            )
            await self.training_service.create_trainings(
                training_plan_id=str(training_plan.id),
                trainings=data.trainings
            )

            await self.training_plan_repository.session.commit()
            await self.training_plan_repository.session.refresh(training_plan)

        except Exception as e:
            await self.training_plan_repository.session.rollback()
            raise

        else:
            training_plan_in_db = await self.training_plan_repository.filter(
                filters={"id": str(training_plan.id)},
                foreign_keys=["customer", "diets", "trainings"]
            )

            return training_plan_in_db[0] if training_plan_in_db else None

    async def find_training_plan(self, filters: dict) -> dict:
        """
        Provides training plan from database in case it is found.

        Args:
            filters: attributes and these values
        """
        foreign_keys, sub_queries = ["trainings"], ["exercises"]
        training_plan = await self.training_plan_repository.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )
        training_plan = training_plan[0]

        training_ids, exercise_ids = [], []
        for training in training_plan.trainings:
            training_ids.append(str(training.id))
            for exercise in training.exercises:
                exercise_ids.append(str(exercise.id))

        scheduled_trainings = await self.training_service.provide_scheduled_trainings(
            training_ids=training_ids,
            exercise_ids=exercise_ids
        )

        if training_plan:
            return {
                "id": str(training_plan.id),
                "start_date": training_plan.start_date.strftime("%Y-%m-%d"),
                "end_date": training_plan.end_date.strftime("%Y-%m-%d"),
                "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
                "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
                "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets]),
                "trainings": [
                    {
                        "id": str(training.id),
                        "name": training.name,
                        "number_of_exercises": len(training_plan.trainings),
                        "exercises": [
                            {
                                "id": str(exercise.id),
                                "name": exercise.name,
                                "sets": scheduled_trainings[str(exercise.id)].sets,
                                "superset_id": str(scheduled_trainings[str(exercise.id)].superset_id),
                                "ordering": scheduled_trainings[str(exercise.id)].ordering
                            }
                            for exercise in training.exercises
                        ]
                    }
                    for training in training_plan.trainings
                ],
                "set_rest": training_plan.set_rest,
                "exercise_rest": training_plan.exercise_rest,
                "notes": training_plan.notes
            }

    async def get_all_customer_training_plans(self, customer_id: str) -> list:
        foreign_keys, sub_queries = ["trainings"], ["exercises"]
        training_plans = await self.training_plan_repository.filter(
            filters={"customer_id": customer_id},
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        return training_plans
