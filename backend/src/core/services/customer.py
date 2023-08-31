from fastapi.security import OAuth2PasswordRequestForm

from src.auth.utils import verify_password
from src.core.repositories.abstract import AbstractRepository
from src.core.services.exceptions import NotValidCredentials
from src.core.services.profile import ProfileService, ProfileType
from src.infrastructure.schemas.auth import UserRegisterIn


class CustomerService(ProfileService):
    """
    Implements logic to interact with Customer domain
    """

    def __init__(self, customer_repo: AbstractRepository):
        self.user = None
        self.user_type = ProfileType.CUSTOMER.value
        self.customer_repo = customer_repo

    async def register(self, data: UserRegisterIn):
        ...

    async def authorize(self, form_data: OAuth2PasswordRequestForm):
        password_in_db = str(self.user.password)
        if password_in_db == form_data.password \
                or await verify_password(form_data.password, password_in_db):
            return self.user

        raise NotValidCredentials

    async def find(self, username: str):
        customer = await self.customer_repo.filter("username", username)
        if customer:
            self.user = customer[0]
            return self.user

    async def update(self, **params):
        await self.handle_profile_photo(params.pop("photo"))
        await self.customer_repo.update(str(self.user.id), **params)
