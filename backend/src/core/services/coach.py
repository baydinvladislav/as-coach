from src.auth.utils import get_hashed_password, verify_password
from src.core.repositories.abstract import AbstractRepository
from src.infrastructure.schemas.auth import CoachRegisterIn


class NotValidPassword(Exception):
    """
    Raises when passed not valid password
    """
    pass


class UsernameIsTaken(Exception):
    """
    Raises when user is trying to register with busy username
    """
    pass


class CoachService:
    """
    Implements logic to interact with Coach domain
    """

    def __init__(self, coach_repo: AbstractRepository):
        self.coach_repo = coach_repo

    async def register_coach(self, data: CoachRegisterIn):
        is_registered = await self.find_by_username(data.username)
        if is_registered:
            raise UsernameIsTaken

        data.password = get_hashed_password(data.password)
        coach = await self.coach_repo.create(**dict(data))

        return coach

    async def find_by_username(self, username: str):
        coach = await self.coach_repo.filter("username", username)
        if coach:
            return coach[0]

    async def authorize(self, coach, passed_password):
        if await verify_password(passed_password, str(coach.password)):
            return True
        else:
            raise NotValidPassword
