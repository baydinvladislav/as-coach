"""
Contains routes for auth service.
"""

import shutil
from datetime import date, datetime
from typing import NewType, Union

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import Gender
from src.auth.schemas import UserProfile
from src.customer.models import Customer
from src.customer.dependencies import get_coach_or_customer

from .dependencies import get_current_user
from .models import User
from .schemas import LoginResponse, UserRegisterIn, UserRegisterOut
from .utils import (create_access_token, create_refresh_token,
                    get_hashed_password, verify_password)
from ..config import STATIC_DIR

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut)
async def create_user(
        user_data: UserRegisterIn,
        database: Session = Depends(get_db)):
    """
    Registration endpoint, creates new user in database

    Args:
        user_data: data schema for user registration
        database: dependency injection for access to database
    Raises:
        400 in case if user with the phone number already created
    Returns:
        dictionary with just created user,
        id, first_name and username as keys
    """
    user = database.query(User).filter(User.username == user_data.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    user = User(
        username=user_data.username,
        first_name=user_data.first_name,
        password=get_hashed_password(user_data.password)
    )

    database.add(user)
    database.commit()

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "username": user.username,
        "access_token": create_access_token(str(user.username)),
        "refresh_token": create_refresh_token(str(user.username))
    }


@auth_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse)
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
    coach = database.query(User).filter(User.username == form_data.username).first()
    customer = database.query(Customer).filter(Customer.username == form_data.username).first()

    user = coach or customer

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not found"
        )

    hashed_password = str(user.password)
    if not verify_password(form_data.password, hashed_password):
        if not customer.password == form_data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

    return {
        "id": str(user.id),
        "user_type": "coach" if coach else "customer",
        "first_name": user.first_name,
        "access_token": create_access_token(str(user.username)),
        "refresh_token": create_refresh_token(str(user.username))
    }


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get details of currently logged in user")
async def get_me(user: Union[User, Customer] = Depends(get_coach_or_customer)):
    """
    Returns info about current user

    Args:
        user: user object from get_current_user dependency

    Returns:
        dictionary with id and username as keys
    """
    return {
        "id": str(user.id),
        "user_type": "coach" if isinstance(user, User) else "customer",
        "username": user.username,
        "first_name": user.first_name
    }


@auth_router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    summary="Get user profile")
async def get_profile(user: Union[User, Customer] = Depends(get_coach_or_customer)):
    """
    Returns full info about user

    Args:
        user: user/customer object from get_coach_or_customer dependency

    Returns:
        dictionary with full user info
    """
    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": "coach" if isinstance(user, User) else "customer",
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_path": user.photo_path
    }


@auth_router.post(
    "/profiles",
    summary="Update user profile",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK)
async def update_profile(
        first_name: str = Form(...),
        username: str = Form(...),
        last_name: str = Form(None),
        photo: UploadFile = File(None),
        gender: NewType('Gender', Gender) = Form(None),
        birthday: date = Form(None),
        email: str = Form(None),
        database: Session = Depends(get_db),
        user: Union[User, Customer] = Depends(get_coach_or_customer)
) -> dict:
    """
    Updated full info about user

    Args:
        first_name: client value from body
        username: client value from body
        last_name: client value from body
        photo: client file from body
        gender: client value from body
        birthday: client value from body
        email: client value from body
        database: dependency injection for access to database
        user: user object from get_current_user dependency

    Returns:
        dictionary with updated full user info
    """
    if photo is not None:
        saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"{user.username}_{saving_time}.jpeg"
        photo_path = f"{STATIC_DIR}/{file_name}"
        with open(photo_path, 'wb') as buffer:
            shutil.copyfileobj(photo.file, buffer)
        user.photo_path = photo_path

    user.modified = datetime.now()

    if isinstance(user, User):
        user_class = User
    else:
        user_class = Customer

    database.query(user_class).filter(user_class.id == str(user.id)).update({
        "first_name": first_name,
        "username": username,
        "last_name": last_name,
        "gender": gender,
        "birthday": birthday,
        "email": email,
    })

    database.commit()
    database.refresh(user)

    if user.photo_path:
        photo_link = user.photo_path.split('/src')[1]
    else:
        photo_link = ""

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": "coach" if isinstance(user, User) else "customer",
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_path": photo_link
    }
