from src.auth.utils import get_hashed_password
from src.core.repositories.abstract import AbstractRepository
from src.infrastructure.schemas.auth import CoachRegisterIn


class UsernameIsTaken(Exception):
    """
    Raises when user is trying to register with busy username
    """
    pass


class CoachService:

    def __init__(self, coach_repo: AbstractRepository):
        self.coach_repo = coach_repo

    async def register_coach(self, data: CoachRegisterIn):
        is_registered = await self.coach_repo.filter("username", data.username)
        if is_registered:
            raise UsernameIsTaken

        data.password = get_hashed_password(data.password)
        coach = await self.coach_repo.create(**dict(data))

        return coach
