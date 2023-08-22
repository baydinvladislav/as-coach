from src.coach.models import Coach
from src.customer.models import Customer
from src.core.repositories.sqlalchemy import SQLAlchemyRepository


class CoachRepository(SQLAlchemyRepository):
    """

    """

    model = Coach


class CustomerRepository(SQLAlchemyRepository):
    """

    """

    model = Customer
