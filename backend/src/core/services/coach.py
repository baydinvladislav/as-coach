from src.auth.utils import get_hashed_password, verify_password
from src.core.repositories.abstract import AbstractRepository
from src.core.services.exceptions import NotValidCredentials, UsernameIsTaken
from src.infrastructure.schemas.auth import CoachRegisterIn


class CoachService:
    """
    Implements logic to interact with Coach domain
    """

    def __init__(self, coach_repo: AbstractRepository):
        self.coach_repo = coach_repo

    async def register_coach(self, data: CoachRegisterIn):
        is_registered = await self.find_coach_by_username(data.username)
        if is_registered:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.coach_repo.create(**dict(data))

        return coach

    @staticmethod
    async def authorize_coach(coach, passed_password):
        password_in_db = str(coach.password)
        if await verify_password(passed_password, password_in_db):
            return True
        else:
            raise NotValidCredentials

    async def find_coach_by_username(self, username: str):
        coach = await self.coach_repo.filter("username", username)
        if coach:
            return coach[0]

    async def update_coach_profile(self, coach, **params):
        self.coach_repo.update(str(coach.id), **params)
