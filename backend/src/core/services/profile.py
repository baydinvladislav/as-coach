from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

import shutil
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.attributes import set_attribute

from src.config import STATIC_DIR
from src.auth.utils import verify_password
from src.infrastructure.schemas.auth import UserRegisterIn


class ProfileType(Enum):
    COACH = "coach"
    CUSTOMER = "customer"


class ProfileService(ABC):
    """
    Abstract for services
    """

    @abstractmethod
    def __init__(self):
        self.user = None
        self.user_type = ""

    @abstractmethod
    async def register(self, data: UserRegisterIn):
        raise NotImplementedError

    @abstractmethod
    async def authorize(self, form_data: OAuth2PasswordRequestForm):
        raise NotImplementedError

    @abstractmethod
    async def find(self, username: str):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **params):
        raise NotImplementedError

    async def handle_profile_photo(self, **params):
        photo = params.pop("photo")
        if photo is not None:
            saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{self.user.username}_{saving_time}.jpeg"
            photo_path = f"{STATIC_DIR}/{file_name}"
            with open(photo_path, 'wb') as buffer:
                shutil.copyfileobj(photo.file, buffer)

            set_attribute(self.user, "photo_path", photo_path)

        set_attribute(self.user, "modified", datetime.now())

    async def confirm_password(self, password) -> bool:
        if await verify_password(password, str(self.user.password)):
            return True
        return False
