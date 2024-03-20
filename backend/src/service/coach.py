import logging

from fastapi.security import OAuth2PasswordRequestForm

from src import Coach
from src.utils import get_hashed_password, verify_password
from src.repository.coach import CoachRepository
from src.shared.exceptions import UsernameIsTaken, NotValidCredentials
from src.service.user import UserService, UserType
from src.schemas.authentication import CoachRegistrationData, UserLoginData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# TODO form Customer aggregate in this layer
class CoachSelectorService:
    def __init__(self, coach_repository: CoachRepository):
        self.coach_repository = coach_repository

    async def select_coach_by_username(self, username: str) -> Coach | None:
        coach = await self.coach_repository.provide_by_username(username)
        return coach


# TODO form Customer aggregate in this layer
class CoachProfileService(UserService):
    def __init__(self, coach_repository: CoachRepository):
        self.coach_repository = coach_repository

    async def register(self, data: CoachRegistrationData) -> Coach | None:
        coach = await self.coach_repository.create(**dict(data))
        return coach

    async def authorize(self, user: Coach, data: UserLoginData) -> bool:
        if await verify_password(data.received_password, user.password):
            if await self.fcm_token_actualize(user, data.fcm_token) is False:
                await self.coach_repository.update(str(user.id), fcm_token=data.fcm_token)
            return True
        return False

    async def update(self, user: Coach, **params) -> None:
        if "photo" in params:
            await self.handle_profile_photo(user, params.pop("photo"))
        await self.coach_repository.update(str(user.id), **params)


class CoachService:

    def __init__(
            self,
            selector_service: CoachSelectorService,
            profile_service: CoachProfileService,
    ):
        self.user = None
        self.user_type = UserType.COACH.value
        self.selector_service = selector_service
        self.profile_service = profile_service

    async def register(self, data: CoachRegistrationData) -> Coach | None:
        existed_coach = await self.selector_service.select_coach_by_username(username=data.username)
        if existed_coach:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.profile_service.register(data)
        if coach:
            self.user = coach
            return coach
        return None

    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Coach | None:
        existed_coach = await self.get_coach_by_username(username=form_data.username)
        if existed_coach is None:
            return None

        logger.info(f"Authorizing coach with username {existed_coach.username}")
        data = UserLoginData(received_password=form_data.password, fcm_token=fcm_token)
        if await self.profile_service.authorize(existed_coach, data) is True:
            logger.info(f"Coach with username {existed_coach.username} successfully login")
            return existed_coach
        raise NotValidCredentials("Not correct coach password")

    async def confirm_password(self, user: Coach, current_password: str) -> bool:
        if await self.profile_service.confirm_password(user, current_password):
            return True
        return False

    async def update(self, user: Coach, **params) -> None:
        await self.profile_service.update(user, **params)

    async def get_coach_by_username(self, username: str) -> Coach | None:
        coach = await self.selector_service.select_coach_by_username(username)
        if coach is not None:
            self.user = coach[0]
            return self.user
        return None
