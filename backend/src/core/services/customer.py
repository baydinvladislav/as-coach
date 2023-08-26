from src.auth.utils import verify_password
from src.core.repositories.abstract import AbstractRepository


class NotValidPassword(Exception):
    """
    Raises when passed not valid password
    """
    pass


class CustomerService:
    """
    Implements logic to interact with Customer domain
    """

    def __init__(self, customer_repo: AbstractRepository):
        self.customer_repo = customer_repo

    @staticmethod
    async def authorize_customer(customer, passed_password):
        password_in_db = str(customer.password)
        if password_in_db == passed_password \
                or await verify_password(passed_password, password_in_db):
            return True
        else:
            raise NotValidPassword

    async def find_customer_by_username(self, username: str):
        customer = await self.customer_repo.filter("username", username)
        if customer:
            return customer[0]

    async def update_customer_profile(self, customer, **params):
        await self.customer_repo.update(str(customer.id), **params)
