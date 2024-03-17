import logging

from fastapi.security import OAuth2PasswordRequestForm

from src import Coach
from src.utils import get_hashed_password, verify_password
from src.repository.coach import CoachRepository
from src.shared.exceptions import NotValidCredentials, UsernameIsTaken
from src.service.authentication.user import UserService, UserType
from src.schemas.authentication import UserLoginData, CoachRegistrationData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CoachSelectorService:
    def __init__(self, coach_repository: CoachRepository) -> None:
        self.coach_repository = coach_repository

    async def get_coach_by_username(self, username: str) -> Coach | None:
        coach = await self.coach_repository.provide_by_username(username)
        return coach[0] if coach is not None else None


class CoachProfileService(UserService):

    def __init__(self, coach_repository: CoachRepository) -> None:
        self.coach_repository = coach_repository

    async def register(self, data: CoachRegistrationData) -> Coach:
        data = {
            "username": data.username,
            "password": await get_hashed_password(data.password),
            "first_name": data.first_name,
            "fcm_token": data.fcm_token,
        }
        coach = await self.coach_repository.create(**data)
        return coach

    async def authorize(self, data: UserLoginData) -> Coach:
        if await verify_password(data.received_password, data.db_password):

            if await self.fcm_token_actualize(data.fcm_token) is False:
                await self.coach_repository.update(str(self.user.id), fcm_token=data.fcm_token)

            return self.user

        raise NotValidCredentials

    async def update(self, user_id: str, photo=None, **params) -> None:
        await self.handle_profile_photo(params.pop("photo"))
        await self.coach_repository.update(str(self.user.id), **params)


class CoachService:

    def __init__(self, profile_service: CoachProfileService, selector_service: CoachSelectorService) -> None:
        self.user = None
        self.user_type = UserType.COACH.value
        self.auth_service = profile_service
        self.selector_service = selector_service

    async def register_coach(self, data: CoachRegistrationData) -> Coach:
        existed_coach = await self.get_coach_by_username(username=data.username)
        if existed_coach:
            logger.warning(f"Customer with username {data.username} already exist")
            raise UsernameIsTaken

        coach = await self.auth_service.register(data)
        return coach

    async def authorize_coach(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Coach | None:
        try:
            coach = await self.auth_service.authorize(
                UserLoginData(
                    user_id=str(self.user.id),
                    db_password=str(self.user.password),
                    received_password=form_data.password,
                    fcm_token=fcm_token,
                )
            )
            logger.info(f"Successfully login coach {coach.username}")
            return coach
        except NotValidCredentials:
            logger.warning(f"Failed user {str(self.user.id)} as coach")
            return None

    async def update_coach(self, **params) -> None:
        coach = await self.auth_service.update(user_id=str(self.user.id), photo=params.pop("photo"), **params)
        return coach

    async def get_coach_by_username(self, username: str) -> Coach | None:
        self.user = await self.selector_service.get_coach_by_username(username)
        return self.user
