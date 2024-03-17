from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

import shutil
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.attributes import set_attribute

from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM, JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
    STATIC_DIR,
)
from src.utils import verify_password
from src.schemas.authentication import UserRegistrationData


class UserType(Enum):
    COACH = "coach"
    CUSTOMER = "customer"


class UserService(ABC):

    @abstractmethod
    def __init__(self):
        self.user = None
        self.user_type = ""

    @abstractmethod
    async def register(self, data: UserRegistrationData):
        raise NotImplementedError

    @abstractmethod
    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **params):
        raise NotImplementedError

    async def generate_jwt_token(self, access: bool = False, refresh: bool = False) -> str:
        if not access and not refresh:
            raise ValueError("Specify what token type you're creating")

        time_delta = timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES) if access else int(REFRESH_TOKEN_EXPIRE_MINUTES)
        )
        expires_delta = datetime.utcnow() + time_delta
        to_encode = {"exp": expires_delta, "sub": str(self.user.username)}
        encoded_jwt = jwt.encode(
            to_encode,
            JWT_SECRET_KEY if access else str(JWT_REFRESH_SECRET_KEY),
            str(ALGORITHM)
        )
        return encoded_jwt

    async def handle_profile_photo(self, photo) -> None:
        if photo is not None:
            saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{self.user.username}_{saving_time}.jpeg"
            photo_path = f"{STATIC_DIR}/{file_name}"
            with open(photo_path, 'wb') as buffer:
                shutil.copyfileobj(photo.file, buffer)

            set_attribute(self.user, "photo_path", photo_path)

    async def confirm_password(self, password: str) -> bool:
        if await verify_password(password, str(self.user.password)):
            return True
        return False

    async def set_fcm_token(self, fcm_token: str) -> None:
        self.user.fcm_token = fcm_token
        set_attribute(self.user, "fcm_token", fcm_token)

    async def fcm_token_actualize(self, fcm_token: str) -> bool:
        if self.user.fcm_token is None or self.user.fcm_token != fcm_token:
            await self.set_fcm_token(fcm_token)
            return True
        else:
            return False
