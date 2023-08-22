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

    async def find_by_username(self, username: str):
        customer = await self.customer_repo.filter("username", username)
        if customer:
            return customer[0]

    async def authorize(self, customer, passed_password: str):
        if customer.password == passed_password \
                or await verify_password(passed_password, str(customer.password)):
            return True
        else:
            raise NotValidPassword
