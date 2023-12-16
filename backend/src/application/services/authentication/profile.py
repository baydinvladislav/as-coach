"""
Template for user services
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

import shutil
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.attributes import set_attribute

from src.config import STATIC_DIR
from src.utils import verify_password
from src.infrastructure.schemas.authentication import UserRegisterIn


class ProfileType(Enum):
    """
    Available application roles
    """
    COACH = "coach"
    CUSTOMER = "customer"


class ProfileService(ABC):
    """
    Abstract class for user services.

    Inherited classes have to implement abstract methods and can use common methods.

    Attributes:
        user: [Coach, Customer]: user ORM instance
        user_type: str: stores role of user
    """

    @abstractmethod
    def __init__(self):
        """
        Assign these empty attrs while find method execution
        """
        self.user = None
        self.user_type = ""

    @abstractmethod
    async def register(self, data: UserRegisterIn):
        """
        Registers new user in application

        Args:
            data: user data for registering passed by client
        """
        raise NotImplementedError

    @abstractmethod
    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str):
        """
        Authorizes user in application

        Args:
            form_data: user credentials passed by client
            fcm_token: token to send push notification on user device
        """
        raise NotImplementedError

    @abstractmethod
    async def find(self, filters: dict):
        """
        Provides user from database in case it is found.
        Save user to user attr.

        Args:
            filters: attributes and these values
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, **params):
        """
        Updates user data in database

        Args:
            params: parameters for user updating
        """
        raise NotImplementedError

    async def handle_profile_photo(self, photo) -> None:
        """
        Saves user profile picture

        Args:
            photo: picture passed by client
        """
        if photo is not None:
            saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{self.user.username}_{saving_time}.jpeg"
            photo_path = f"{STATIC_DIR}/{file_name}"
            with open(photo_path, 'wb') as buffer:
                shutil.copyfileobj(photo.file, buffer)

            set_attribute(self.user, "photo_path", photo_path)

    async def confirm_password(self, password: str) -> bool:
        """
        Confirms that user know password

        Used before password changing

        Args:
            password: current user password
        """
        if await verify_password(password, str(self.user.password)):
            return True
        return False

    async def set_fcm_token(self, fcm_token: str) -> None:
        """
        Assign Firebase token to user.

        Args:
            fcm_token: device token to identify receiver a push notification
        """
        self.user.fcm_token = fcm_token
        set_attribute(self.user, "fcm_token", fcm_token)
