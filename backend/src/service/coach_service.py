import logging

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import Coach
from src.schemas.coach_dto import CoachDtoSchema
from src.utils import get_hashed_password, verify_password
from src.repository.coach_repository import CoachRepository
from src.shared.exceptions import UsernameIsTaken, NotValidCredentials
from src.service.user_service import UserService, UserType
from src.presentation.schemas.authentication_schema import CoachRegistrationData, UserLoginData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CoachSelectorService:
    """Responsible for getting coach data from storage"""

    def __init__(self, coach_repository: CoachRepository) -> None:
        self.coach_repository = coach_repository

    async def select_coach_by_username(self, uow: AsyncSession, username: str) -> CoachDtoSchema | None:
        coach = await self.coach_repository.provide_by_username(uow, username)
        return coach


class CoachProfileService(UserService):
    """Responsible for coach profile operations"""

    def __init__(self, coach_repository: CoachRepository) -> None:
        self.coach_repository = coach_repository

    async def register_user(self, uow: AsyncSession, data: CoachRegistrationData) -> CoachDtoSchema | None:
        coach = await self.coach_repository.create_coach(uow, data)
        return coach

    async def authorize_user(self, uow: AsyncSession, user: CoachDtoSchema, data: UserLoginData) -> bool:
        if await verify_password(data.received_password, user.password):
            if await self.fcm_token_actualize(user, data.fcm_token) is False:
                await self.coach_repository.update_coach(uow, id=str(user.id), fcm_token=data.fcm_token)
            return True
        return False

    async def update_user_profile(self, uow: AsyncSession, user: Coach, **params) -> CoachDtoSchema | None:
        if "photo" in params:
            await self.handle_profile_photo(user, params.pop("photo"))

        updated_profile = await self.coach_repository.update_coach(uow, id=str(user.id), **params)
        return updated_profile

    async def delete(self, uow: AsyncSession, user: Coach) -> str | None:
        deleted_id = await self.coach_repository.delete_coach(uow, str(user.id))
        return deleted_id


class CoachService:
    """Contains business rules for Coach subdomain"""

    def __init__(self, selector_service: CoachSelectorService, profile_service: CoachProfileService) -> None:
        self.user = None
        self.user_type = UserType.COACH.value
        self.selector_service = selector_service
        self.profile_service = profile_service

    async def register_coach(self, uow: AsyncSession, data: CoachRegistrationData) -> CoachDtoSchema | None:
        existed_coach = await self.selector_service.select_coach_by_username(uow, username=data.username)
        if existed_coach:
            raise UsernameIsTaken

        data.password = await get_hashed_password(data.password)
        coach = await self.profile_service.register_user(uow, data)
        if coach:
            self.user = coach
            return coach
        return None

    async def authorize_coach(
        self,
        uow: AsyncSession,
        form_data: OAuth2PasswordRequestForm,
        fcm_token: str
    ) -> CoachDtoSchema | None:
        existed_coach = await self.get_coach_by_username(uow, username=form_data.username)
        if existed_coach is None:
            return None

        logger.info(f"Authorizing coach with username {existed_coach.username}")
        data = UserLoginData(received_password=form_data.password, fcm_token=fcm_token)
        if await self.profile_service.authorize_user(uow, existed_coach, data) is True:
            logger.info(f"Coach with username {existed_coach.username} successfully login")
            return existed_coach
        raise NotValidCredentials("Not correct coach password")

    async def confirm_coach_password(self, user: Coach, current_password: str) -> bool:
        if await self.profile_service.confirm_password(user, current_password):
            return True
        return False

    async def update_profile(self, uow: AsyncSession, user: Coach, **params) -> CoachDtoSchema | None:
        updated_coach = await self.profile_service.update_user_profile(uow, user, **params)
        return updated_coach

    async def delete(self, uow: AsyncSession, user: Coach) -> str | None:
        deleted_id = await self.profile_service.delete(uow, user)
        if deleted_id is None:
            logger.info(f"Couldn't delete coach {user.username}")
            return
        logger.info(f"Coach {user.username} successfully deleted")

    async def get_coach_by_username(self, uow: AsyncSession, username: str) -> CoachDtoSchema | None:
        coach = await self.selector_service.select_coach_by_username(uow, username)
        if coach is not None:
            self.user = coach
            return self.user
        return None
