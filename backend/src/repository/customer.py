from sqlalchemy import select, func, nullsfirst, and_

from src import Customer, TrainingPlan
from src.repository.base import BaseRepository


class CustomerRepository(BaseRepository):
    """
    Access to Customer storage
    """
    model = Customer

    async def provide_by_username(self, username: str) -> Customer | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        customer = result.fetchone()
        return customer

    async def provide_by_full_name(self, first_name: str, last_name: str) -> Customer | None:
        query = select(self.model).where(
            and_(
                self.model.first_name == first_name, self.model.last_name == last_name
            )
        )
        result = await self.session.execute(query)
        customer = result.fetchone()
        return customer

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
