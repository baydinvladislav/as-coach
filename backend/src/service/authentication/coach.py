from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from src import Coach
from src.utils import get_hashed_password, verify_password
from src.repository.coach import CoachRepository
from src.service.authentication.exceptions import NotValidCredentials, UsernameIsTaken
from src.service.authentication.user import UserService, UserType
from src.schemas.authentication import UserRegisterIn


class CoachService(UserService):

    def __init__(self, coach_repository: CoachRepository):
        self.user = None
        self.user_type = UserType.COACH.value
        self.coach_repository = coach_repository

    async def register(self, data: UserRegisterIn) -> Coach:
        existed_coach = await self.get_coach_by_username(username=data.username)
        if existed_coach:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.coach_repository.create(**dict(data))
        return coach

    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Coach:
        password_in_db = str(self.user.password)
        if await verify_password(form_data.password, password_in_db):

            # to update User.fcm_token
            if self.user.fcm_token != fcm_token:
                await self.set_fcm_token(fcm_token)
                await self.coach_repository.update(str(self.user.id), fcm_token=fcm_token)

            return self.user

        raise NotValidCredentials

    async def update(self, **params) -> None:
        await self.handle_profile_photo(params.pop("photo"))
        await self.coach_repository.update(str(self.user.id), **params)

    async def get_coach_by_username(self, username: str) -> Coach | None:
        coach = await self.coach_repository.provide_by_username(username)

        if coach:
            self.user = coach[0]
            return self.user

    # deprecating...
    async def find(self, filters: dict) -> Optional[Coach]:
        foreign_keys, sub_queries = ["customers"], ["training_plans"]
        coach = await self.coach_repository.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if coach:
            self.user = coach[0]
            return self.user
