from src.coach.models import Coach
from src.customer.models import Customer
from src.core.repositories.sqlalchemy import SQLAlchemyRepository


class CoachRepository(SQLAlchemyRepository):
    """
    Access to Coach domain
    """

    model = Coach


class CustomerRepository(SQLAlchemyRepository):
    """
    Access to Customer domain
    """

    model = Customer
