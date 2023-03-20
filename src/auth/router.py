"""
Contains routes for auth service.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from .dependencies import get_current_user
from .models import User
from .schemas import TokenSchema, UserRegisterIn, UserRegisterOut
from .utils import (create_access_token, create_refresh_token,
                            get_hashed_password, verify_password)

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut)
async def create_user(
        data: UserRegisterIn,
        database: Session = Depends(get_db)):
    """
    Registration endpoint, creates new user in database

    Args:
        data: data schema for user registration
        database: dependency injection for access to database
    Raises:
        400 in case if user with the phone number already created
    Returns:
        dictionary with just created user, id and username as keys
    """
    user = database.query(User).filter(User.username == data.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    user = User(
        username=data.username,
        password=get_hashed_password(data.password)
    )

    database.add(user)
    database.commit()

    return {
        "id": str(user.id),
        "username": user.username
    }


@auth_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        database: Session = Depends(get_db)):
    """
    Login endpoint authenticates user

    Args:
        form_data: data schema for user login
        database: dependency injection for access to database
    Raises:
        404 if specified user was not found
        400 in case if user is found but password does not match
    Returns:
        access_token and refresh_token inside dictionary
    """
    user = database.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not found"
        )

    hashed_password = str(user.password)
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(str(user.username)),
        "refresh_token": create_refresh_token(str(user.username))
    }


@auth_router.get(
    "/me",
    summary='Get details of currently logged in user')
async def get_me(user: User = Depends(get_current_user)):
    """
    Returns info about current user

    Args:
        user: user object from get_current_user dependency

    Returns:
        dictionary with id and username as keys
    """
    return {"id": str(user.id), "username": user.username}
