"""
Service for Customer role functionality
"""

from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from src.customer.models import Customer
from src.auth.utils import verify_password
from src.core.repositories.abstract import AbstractRepository
from src.core.services.exceptions import NotValidCredentials
from src.core.services.profile import ProfileService, ProfileType
from src.infrastructure.schemas.auth import UserRegisterIn


class CustomerService(ProfileService):
    """
    Implements logic to interact with Customer domain

    Attributes:
        user: Customer: customer ORM instance
        user_type: str: mark as customer role
        customer_repo: repository to interacting with storage using customer domain
    """

    def __init__(self, customer_repo: AbstractRepository):
        self.user = None
        self.user_type = ProfileType.CUSTOMER.value
        self.customer_repo = customer_repo

    async def register(self, data: UserRegisterIn) -> Customer:
        """
        Temperately customer registration implemented by Coach's invites
        """
        ...

    async def authorize(self, form_data: OAuth2PasswordRequestForm) -> Customer:
        """
        Customer logs in with default password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.

        Args:
            form_data: customer credentials passed by client

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        password_in_db = str(self.user.password)
        if password_in_db == form_data.password \
                or await verify_password(form_data.password, password_in_db):
            return self.user

        raise NotValidCredentials

    async def find(self, filters: dict) -> Optional[Customer]:
        """
        Provides customer from database in case it is found.
        Save customer instance to user attr.

        Args:
            filters: attributes and these values
        """
        foreign_keys, sub_queries = ["training_plans"], ["trainings", "diets"]
        customer = await self.customer_repo.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if customer:
            self.user = customer[0]
            return self.user

    # TODO: return numbers of updated rows
    async def update(self, **params) -> None:
        """
        Updates customer data in database

        Args:
            params: parameters for customer updating
        """
        await self.handle_profile_photo(params.pop("photo"))
        await self.customer_repo.update(str(self.user.id), **params)

    async def create(self, coach_id: str, **kwargs) -> Customer:
        """
        Creates new customer in database

        Args:
            coach_id: customer's coach
            kwargs: any required params for customer creating

        Returns:
            customer: Customer instance
        """
        customer = await self.customer_repo.create(coach_id=coach_id, **kwargs)
        return customer
