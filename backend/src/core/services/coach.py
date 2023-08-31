from fastapi.security import OAuth2PasswordRequestForm

from src.auth.utils import get_hashed_password, verify_password
from src.core.repositories.abstract import AbstractRepository
from src.core.services.exceptions import NotValidCredentials, UsernameIsTaken
from src.core.services.profile import ProfileService, ProfileType
from src.infrastructure.schemas.auth import UserRegisterIn


class CoachService(ProfileService):
    """
    Implements logic to interact with Coach domain
    """

    def __init__(self, coach_repo: AbstractRepository):
        self.user = None
        self.user_type = ProfileType.COACH.value
        self.coach_repo = coach_repo

    async def register(self, data: UserRegisterIn):
        is_registered = await self.find(data.username)
        if is_registered:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.coach_repo.create(**dict(data))

        return coach

    async def authorize(self, form_data: OAuth2PasswordRequestForm):
        password_in_db = str(self.user.password)
        if await verify_password(form_data.password, password_in_db):
            return self.user

        raise NotValidCredentials

    async def find(self, username: str):
        coach = await self.coach_repo.filter("username", username)
        if coach:
            self.user = coach[0]
            return self.user

    async def update(self, **params):
        await self.handle_profile_photo(params.pop("photo"))
        await self.coach_repo.update(str(self.user.id), **params)
