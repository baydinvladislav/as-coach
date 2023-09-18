"""
Contains services related to the Gym functionality
"""

from datetime import datetime

from src.core.usecases.services.gym.instructor import Instructor
from src.core.usecases.services.gym.nutritionist import Nutritionist
from src.core.repositories.abstract import AbstractRepository
from src.interfaces.schemas.customer import TrainingPlanIn
from src import TrainingPlan


class Gym:
    """
    The service to provide fitness services for customers.

    Attributes:
        training_plan_repo: repository to store TrainingPlan rows
        gym_instructor: the service responsible for trainings operations
        nutritionist: the service responsible for diets operations
    """

    def __init__(
            self,
            repositories: dict[str, AbstractRepository],
            gym_instructor: Instructor,
            nutritionist: Nutritionist
    ):
        self.training_plan_repo = repositories["training_plan"]
        self.gym_instructor = gym_instructor
        self.nutritionist = nutritionist

    async def create_training_plan(self, customer_id: str, data: TrainingPlanIn) -> TrainingPlan:
        """
        Creates training plan for customer

        Args:
            customer_id: UUID of the customer for whom the training plan is being created
            data: data from client for creating new training plan
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
        Provides training plan from database in case it is found.

        Args:
            filters: attributes and these values
        """
        foreign_keys, sub_queries = ["trainings"], ["exercises"]
        training_plan = await self.training_plan_repo.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if training_plan:
            return training_plan[0]
