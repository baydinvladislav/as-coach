"""
Contains abstract training manager
"""

from abc import ABC
from typing import Optional

from src.infrastructure.schemas.customer import TrainingPlanIn
from src import TrainingPlan


class TrainingManagerInterface(ABC):
    """
    Interface for training managers
    """

    async def create_training_plan(self, customer_id: str, data: TrainingPlanIn) -> TrainingPlan:
        """
        Creates training plan for customer

        Args:
            customer_id: UUID of the customer for whom the training plan is being created
            data: data from client for creating new training plan
        """
        raise NotImplementedError

    async def find_training_plan(self, filters: dict) -> Optional[TrainingPlan]:
        """
        Provides some training plan from database in case it is found.

        Args:
            filters: attributes and these values
        """
        raise NotImplementedError

    async def get_all_customer_training_plans(self, customer_id: str) -> list:
        """
        Gets available training plans for specific customer.

        Args:
            customer_id: customer row UUID
        """
