"""
Service for Coach role functionality
"""

from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from src.coach.models import Coach
from src.auth.utils import get_hashed_password, verify_password
from src.core.repositories.abstract import AbstractRepository
from src.core.services.exceptions import NotValidCredentials, UsernameIsTaken
from src.core.services.profile import ProfileService, ProfileType
from src.infrastructure.schemas.auth import UserRegisterIn


class CoachService(ProfileService):
    """
    Implements logic to interact with Coach user role

    Attributes:
        user: Coach: coach ORM instance
        user_type: str: mark as coach role
        coach_repo: repository to interacting with storage using coach domain
    """

    def __init__(self, coach_repo: AbstractRepository):
        self.user = None
        self.user_type = ProfileType.COACH.value
        self.coach_repo = coach_repo

    async def register(self, data: UserRegisterIn) -> Coach:
        """
        Registers new coach in application

        Args:
            data: data for registration passed by client
        """
        is_registered = await self.find(data.username)
        if is_registered:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.coach_repo.create(**dict(data))

        return coach

    async def authorize(self, form_data: OAuth2PasswordRequestForm) -> Coach:
        """
        Coach logs in with own hashed password.

        Args:
            form_data: coach credentials passed by client

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        password_in_db = str(self.user.password)
        if await verify_password(form_data.password, password_in_db):
            return self.user

        raise NotValidCredentials

    async def find(self, username: str) -> Optional[Coach]:
        """
        Provides coach from database in case it is found.
        Save coach instance to user attr.

        Args:
            username: coach phone number passed by client
        """
        coach = await self.coach_repo.filter("username", username)
        if coach:
            self.user = coach[0]
            return self.user

    async def update(self, **params) -> None:
        """
        Updates coach data in database

        Args:
            params: parameters for coach updating
        """
        await self.handle_profile_photo(params.pop("photo"))
        await self.coach_repo.update(str(self.user.id), **params)
