from sqlalchemy import select, func, nullsfirst, and_, literal_column
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.dialects.postgresql import insert

from src import Customer, TrainingPlan
from src.repository.base_repository import BaseRepository
from src.schemas.authentication_schema import CustomerRegistrationData
from src.schemas.customer_schema import CustomerOut


class CustomerRepository(BaseRepository):
    async def create(self, db_session: Session, data: CustomerRegistrationData) -> CustomerOut | None:
        statement = (
            insert(Customer)
            .values(
                coach_id=data.coach_id,
                telegram_username=data.telegram_username,
                first_name=data.first_name,
                last_name=data.last_name,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = db_session.execute(statement).fetchone()
        if result is None:
            return None

        return CustomerOut.from_orm(result)

    async def provide_by_pk(self, pk: str) -> Customer | None:
        query = (
            select(Customer).where(Customer.id == pk)
            .options(
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.trainings),
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.diets)
            )
        )

        result = await self.session.execute(query)
        customer = result.scalar_one_or_none()
        return customer

    async def provide_by_otp(self, password: str) -> Customer | None:
        query = (
            select(Customer).where(Customer.password == password)
        .options(
            selectinload(Customer.training_plans).subqueryload(TrainingPlan.trainings),
            selectinload(Customer.training_plans).subqueryload(TrainingPlan.diets)
        ))

        result = await self.session.execute(query)
        customer = result.scalar_one_or_none()
        return customer

    async def provide_by_username(self, username: str) -> Customer | None:
        query = (
            select(Customer).where(Customer.username == username)
        )
        result = await self.session.execute(query)
        customer = result.fetchone()
        return customer

    async def provide_by_coach_id_and_full_name(
        self, coach_id: str, first_name: str, last_name: str
    ) -> Customer | None:
        query = (
            select(Customer).where(
                and_(
                    Customer.coach_id == coach_id,
                    Customer.first_name == first_name,
                    Customer.last_name == last_name,
                )
            )
        )
        result = await self.session.execute(query)
        customer = result.fetchone()
        return customer

    async def provide_customers_by_coach_id(self, coach_id: str) -> list[Customer]:
        query = (
            select(
                Customer.id,
                Customer.first_name,
                Customer.last_name,
                Customer.username,
                func.max(TrainingPlan.end_date).label("last_plan_end_date")
            )
            .join(TrainingPlan, Customer.id == TrainingPlan.customer_id, isouter=True)
            .where(Customer.coach_id == coach_id)
            .group_by(Customer.id)
            .order_by(nullsfirst(func.max(TrainingPlan.end_date).asc()))
        )

        result = await self.session.execute(query)
        return result.fetchall()
