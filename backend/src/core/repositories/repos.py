from src.coach.models import Coach
from src.core.repositories.sqlalchemy import SQLAlchemyRepository


class CoachRepository(SQLAlchemyRepository):
    """

    """

    model = Coach
