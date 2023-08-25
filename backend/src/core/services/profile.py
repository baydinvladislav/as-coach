from datetime import datetime
from enum import Enum

import shutil
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.attributes import set_attribute

from src.auth.utils import verify_password
from src.config import STATIC_DIR
from src.core.services.coach import CoachService
from src.core.services.customer import CustomerService
from src.core.services.exceptions import UserDoesNotExist
from src.infrastructure.schemas.auth import CoachRegisterIn


class ProfileType(Enum):
    COACH = "coach"
    CUSTOMER = "customer"


class ProfileService:

    def __init__(self, coach_service: CoachService, customer_service: CustomerService):
        self.coach_service = coach_service
        self.customer_service = customer_service
        self.username = ""
        self.user_type = ""

    async def authorize_user(self, form_data: OAuth2PasswordRequestForm):
        user = await self.get_current_user(form_data.username)

        if self.user_type == ProfileType.COACH.value:
            await self.coach_service.authorize_coach(user, form_data.password)
            return user
        elif self.user_type == ProfileType.CUSTOMER.value:
            await self.customer_service.authorize_customer(user, form_data.password)
            return user
        else:
            raise UserDoesNotExist

    async def register_user(self, data: CoachRegisterIn):
        coach = await self.coach_service.register_coach(data)
        return coach

    async def get_current_user(self, username):
        coach = await self.coach_service.find_coach_by_username(username)
        customer = await self.customer_service.find_customer_by_username(username)

        if coach is not None:
            self.user_type = ProfileType.COACH.value
        elif customer is not None:
            self.user_type = ProfileType.CUSTOMER.value
        else:
            raise UserDoesNotExist

        self.username = username
        user = coach or customer

        if user is None:
            raise UserDoesNotExist

        return user

    async def update_user_profile(self, user, **params):
        user_updated = False

        if params.get("photo") is not None:
            saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{user.username}_{saving_time}.jpeg"
            photo_path = f"{STATIC_DIR}/{file_name}"
            with open(photo_path, 'wb') as buffer:
                shutil.copyfileobj(params.get("photo").file, buffer)

            set_attribute(user, "photo_path", photo_path)

        set_attribute(user, "modified", datetime.now())

        if self.user_type == ProfileType.COACH:
            await self.coach_service.update_coach_profile(coach=user, **params)
            user_updated = True
        elif self.user_type == ProfileType.CUSTOMER:
            await self.customer_service.update_customer_profile(customer=user, **params)
            user_updated = True

        return user_updated

    @staticmethod
    async def confirm_user_password(password, user) -> bool:
        if verify_password(password, str(user.password)):
            return True
        return False

    async def change_password(self, new_password, user):
        ex_password = user.password

        if self.user_type == ProfileType.COACH:
            await self.coach_service.update_coach_profile(user, password=new_password)
        elif self.user_type == ProfileType.CUSTOMER:
            await self.customer_service.update_customer_profile(user, password=new_password)

        return bool(ex_password != user.password)
