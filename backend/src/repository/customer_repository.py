from sqlalchemy import select, delete, update, func, nullsfirst, and_, literal_column
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.dialects.postgresql import insert

from src import Customer, TrainingPlan
from src.schemas.authentication_schema import CustomerRegistrationData
from src.schemas.user_coach_schema import UserCustomerSchema, UserCustomerShort


class CustomerRepository:
    # TODO: AsyncSession
    async def create_customer(self, uow: Session, data: CustomerRegistrationData) -> UserCustomerSchema | None:
        statement = (
            insert(Customer)
            .values(
                coach_id=data.coach_id,
                telegram_username=data.telegram_username,
                first_name=data.first_name,
                password=data.password,
                last_name=data.last_name,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        customer_id = result.scalar_one_or_none()

        if customer_id is None:
            return None

        customer = await self.provide_by_pk(uow, str(customer_id))
        return UserCustomerSchema.from_orm(customer)

    async def update_customer(self, uow: Session, **kwargs) -> UserCustomerSchema | None:
        statement = (
            update(Customer)
            .where(Customer.id == kwargs["id"])
            .values(**kwargs)
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        coach = result.fetchone()

        if coach is None:
            return None

        return UserCustomerSchema.from_orm(coach)

    async def delete_customer(self, uow: Session, pk: str) -> str | None:
        stmt = delete(Customer).where(Customer.id == pk)
        result = await uow.execute(stmt)
        uow.commit()

        if result.rowcount == 0:
            return None

        return pk

    async def provide_by_pk(self, uow: Session, pk: str) -> UserCustomerSchema | None:
        query = (
            select(Customer).where(Customer.id == pk)
            .options(
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.trainings),
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.diets)
            )
        )

        result = await uow.execute(query)
        customer = result.scalar_one_or_none()

        if customer is None:
            return None

        return UserCustomerSchema.from_orm(customer)

    async def provide_by_otp(self, uow: Session, password: str) -> UserCustomerSchema | None:
        query = (
            select(Customer).where(Customer.password == password)
            .options(
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.trainings),
                selectinload(Customer.training_plans).subqueryload(TrainingPlan.diets)
            )
        )

        result = await uow.execute(query)
        customer = result.scalar_one_or_none()

        if customer is None:
            return None

        return UserCustomerSchema.from_orm(customer)

    async def provide_by_username(self, uow: Session, username: str) -> UserCustomerSchema | None:
        query = (
            select(Customer).where(Customer.username == username)
        )
        result = await uow.execute(query)
        customer = result.fetchone()

        if customer is None:
            return None

        return UserCustomerSchema.from_orm(customer)

    async def provide_by_coach_id_and_full_name(
        self, uow: Session, coach_id: str, first_name: str, last_name: str
    ) -> UserCustomerSchema | None:
        query = (
            select(Customer).where(
                and_(
                    Customer.coach_id == coach_id,
                    Customer.first_name == first_name,
                    Customer.last_name == last_name,
                )
            )
        )
        result = await uow.execute(query)
        customer = result.fetchone()

        if customer is None:
            return None

        return UserCustomerSchema.from_orm(customer)

    async def provide_customers_by_coach_id(self, uow: Session, coach_id: str) -> list[UserCustomerShort]:
        query = (
            select(
                Customer.id,
                Customer.first_name,
                Customer.coach_id,
                Customer.password,
                Customer.last_name,
                Customer.username,
                func.max(TrainingPlan.end_date).label("last_plan_end_date")
            )
            .join(TrainingPlan, Customer.id == TrainingPlan.customer_id, isouter=True)
            .where(Customer.coach_id == coach_id)
            .group_by(Customer.id)
            .order_by(nullsfirst(func.max(TrainingPlan.end_date).asc()))
        )

        result = await uow.execute(query)
        customers = result.fetchall()
        return [UserCustomerShort.from_orm(customer) for customer in customers]
