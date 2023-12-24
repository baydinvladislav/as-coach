from src import DietOnTrainingPlan
from src.repository.abstract import AbstractRepository


class Nutritionist:
    """
    The service responsible for diets operations

    Attributes:
        diet_repo: repository to store Diet rows
        diets_on_training_repo: repository to store DietsOnTrainingPlan rows
    """

    def __init__(self, repositories: dict[str, AbstractRepository]):
        self.diet_repo = repositories["diet_repo"]
        self.diets_on_training_repo = repositories["diets_on_training_repo"]

    async def create_diets(self, training_plan_id: str, diets: list):
        """
        Creates diets in customer training plan

        Args:
            training_plan_id: UUID of training plan
            diets: data for creating diets
        """
        for diet_data in diets:
            diet = await self.diet_repo.create(
                proteins=diet_data.proteins,
                fats=diet_data.fats,
                carbs=diet_data.carbs
            )

            self.diet_repo.session.add(diet)
            await self.diet_repo.session.flush()

            diet_on_training_plan = DietOnTrainingPlan(
                diet_id=str(diet.id),
                training_plan_id=training_plan_id
            )
            self.diet_repo.session.add(diet_on_training_plan)
