from sqlalchemy import select, func, nullsfirst

from src import Customer, TrainingPlan
from src.repository.sqlalchemy import SQLAlchemyRepository


class CustomerRepository(SQLAlchemyRepository):
    """
    Access to Customer storage
    """
    model = Customer

    async def provide_customers_by_coach_id(self, coach_id: str):
        query = (
            select(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.username,
                func.max(TrainingPlan.end_date).label('last_plan_end_date')
            )
            .join(TrainingPlan, self.model.id == TrainingPlan.customer_id, isouter=True)
            .where(self.model.coach_id == coach_id)
            .group_by(self.model.id)
            .order_by(nullsfirst(func.max(TrainingPlan.end_date).asc()))
        )

        result = await self.session.execute(query)
        return result.fetchall()
