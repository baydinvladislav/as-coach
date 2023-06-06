"""
Module for auth utils
"""

from datetime import datetime, timedelta

from jose import jwt
from fastapi import HTTPException, status
from pydantic import ValidationError
from passlib.context import CryptContext

from backend.src.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_REFRESH_SECRET_KEY,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Hashes password

    Args:
        password: string which will be hashed

    Returns:
        hashed password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
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


def create_access_token(subject: str) -> str:
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


def create_refresh_token(subject: str) -> str:
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


def decode_jwt_token(token: str):
    """
    Decodes given token
    """
    # TODO: fix it
    from src.auth.schemas import TokenPayload

    try:
        payload = jwt.decode(
            token, str(JWT_SECRET_KEY), algorithms=[str(ALGORITHM)]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return token_data

    except (jwt.JWTError, ValidationError):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def validate_password(password: str):
    """
    Password can be at least 8 characters
    """
    if 7 < len(password) < 129:
        return password
    raise ValueError("Password must be greater than 7 symbols and less than 129 symbols")
