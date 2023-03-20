"""
Module for auth utils
"""

from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from src.auth.config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                             JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY,
                             REFRESH_TOKEN_EXPIRE_MINUTES)

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
    return password_context.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Creates access token

    Args:
        subject: user's username

    Returns:
        access token
    """
    expires_delta = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))  # type: ignore
    to_encode = {"exp": expires_delta, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    """
    Creates refresh token

    Args:
        subject: user's username

    Returns:
        refresh token
    """
    expires_delta = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))  # type: ignore
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
