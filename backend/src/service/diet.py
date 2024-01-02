from src import DietOnTrainingPlan
from src.repository.abstract import AbstractRepository
from src.repository.diet import DietRepository, DietsInTrainingPlanRepository


# class DietService:
#     diet_repository: DietRepository
#     diets_in_training_plan_repository: DietsInTrainingPlanRepository
#
#     async def create_diet(self):
#         ...
#
#     async def get_diets_by_training_plan_id(self):
#         ...


class DietService:
    """
    The service responsible for diets operations

    Attributes:
        diet_repository: repository to store Diet rows
        diets_on_training_repository: repository to store DietsOnTrainingPlan rows
    """

    def __init__(self, repositories: dict[str, AbstractRepository]):
        self.diet_repository = repositories["diet_repo"]
        self.diets_on_training_repository = repositories["diets_on_training_repo"]

    async def create_diets(self, training_plan_id: str, diets: list):
        """
        Creates diets in customer training plan

        Args:
            training_plan_id: UUID of training plan
            diets: data for creating diets
        """
        for diet_data in diets:
            diet = await self.diet_repository.create(
                proteins=diet_data.proteins,
                fats=diet_data.fats,
                carbs=diet_data.carbs
            )

            self.diet_repository.session.add(diet)
            await self.diet_repository.session.flush()

            diet_on_training_plan = DietOnTrainingPlan(
                diet_id=str(diet.id),
                training_plan_id=training_plan_id
            )
            self.diet_repository.session.add(diet_on_training_plan)
