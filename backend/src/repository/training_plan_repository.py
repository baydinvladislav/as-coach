from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from src import TrainingPlan, Training
from src.repository.base_repository import BaseRepository


class TrainingPlanRepository(BaseRepository):
    model = TrainingPlan

    async def provide_customer_plans_by_customer_id(self, customer_id: str) -> list[TrainingPlan]:
        query = select(self.model).where(
            self.model.customer_id == customer_id
        ).options(
            selectinload(self.model.trainings).subqueryload(Training.exercises),
        ).order_by(
            desc(self.model.end_date)
        )

        training_plans = await self.session.scalars(query)
        return training_plans
