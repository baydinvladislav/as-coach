"""
Common utils for project
"""
import random
import string

import uuid
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES, \
    JWT_REFRESH_SECRET_KEY
from src.core.services.exceptions import TokenExpired, NotValidCredentials

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_phone_number(phone_number: str):
    """
    We have to get: +79xxxxxxxxx
    Phone number must contain 12 numbers
    """
    if phone_number.startswith("+7") and len(phone_number) == 12:
        return phone_number
    raise ValueError("Specify correct phone number")


async def validate_uuid(uuid_value: str):
    """
    Validates passed uuid
    """
    try:
        uuid.UUID(str(uuid_value))
        return True
    except ValueError:
        return False


async def get_hashed_password(password: str) -> str:
    """
    Hashes password

    Args:
        password: string which will be hashed

    Returns:
        hashed password
    """
    return password_context.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks that string is hashed string

    Args:
        password: row password from client request
        hashed_password: hashed password from database user profile

    Returns:
        True if password matches with hashed_password otherwise False
    """
    is_identified = password_context.identify(hashed_password)
    if not is_identified:
        return False

    is_verified = password_context.verify(password, hashed_password)
    if is_verified:
        return True
    return False


async def create_access_token(subject: str) -> str:
    """
    Creates access token

    Args:
        subject: user's username

    Returns:
        access token
    """
    time_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))  # type: ignore
    expires_delta = datetime.utcnow() + time_delta
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(JWT_SECRET_KEY), str(ALGORITHM))
    return encoded_jwt


async def create_refresh_token(subject: str) -> str:
    """
    Creates refresh token

    Args:
        subject: user's username

    Returns:
        refresh token
    """
    time_delta = timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))  # type: ignore
    expires_delta = datetime.utcnow() + time_delta
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(JWT_REFRESH_SECRET_KEY), str(ALGORITHM))
    return encoded_jwt


async def decode_jwt_token(token: str):
    """
    Decodes given token
    """
    # TODO: fix it
    from src.interfaces.schemas.auth import TokenPayload

    try:
        payload = jwt.decode(
            token, str(JWT_SECRET_KEY), algorithms=[str(ALGORITHM)]
        )
        token_data = TokenPayload(**payload)

        expiration_time = datetime.fromtimestamp(token_data.exp)
        if expiration_time < datetime.now():
            raise TokenExpired

        return token_data

    except (jwt.JWTError, ValidationError):  # type: ignore
        raise NotValidCredentials


def validate_password(password: str):
    """
    Password can be at least 8 characters
    """
    if 7 < len(password) < 129:
        return password
    raise ValueError("Password must be greater than 7 symbols and less than 129 symbols")


def generate_random_password(length: int) -> str:
    """
    Generates a random password of a given length
    Args:
       length: length of result password
    """
    letters = string.ascii_letters + string.digits
    password = "".join(random.choice(letters) for _ in range(length))
    return password
