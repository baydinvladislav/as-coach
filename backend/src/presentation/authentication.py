"""
Contains controllers for user functionality
"""

from datetime import date
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src.service.authentication.coach import CoachService
from src.service.authentication.customer import CustomerService
from src.service.authentication.profile import ProfileService
from src.service.authentication.exceptions import NotValidCredentials, UsernameIsTaken
from src.dependencies import provide_user_service, provide_coach_service, provide_customer_service
from src.persistence.models import Gender
from src.schemas.authentication import (
    UserProfileOut,
    NewUserPassword,
    LoginOut,
    UserRegisterIn,
    UserRegisterOut
)
from src.utils import password_context, create_access_token, create_refresh_token

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut)
async def register_user(
        user_data: UserRegisterIn,
        service: CoachService = Depends(provide_coach_service)
) -> dict:
    """
    Registration endpoint, creates new user in database.
    Registration for customers implemented through adding coach's invites.

    Args:
        user_data: data schema for user registration
        service: service for interacting with profile
    Raises:
        400 in case if user with the phone number already created
    Returns:
        dictionary with just created user
    """
    try:
        user = await service.register(user_data)
    except UsernameIsTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with phone number: {user_data.username} already exists"
        )

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "username": user.username,
        "access_token": await create_access_token(str(user.username)),
        "refresh_token": await create_refresh_token(str(user.username))
    }


@auth_router.post(
    "/login",
    summary="Authorizes any user, both trainer and customer",
    status_code=status.HTTP_200_OK,
    response_model=LoginOut)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        fcm_token: str = Form(...),
        coach_service: CoachService = Depends(provide_coach_service),
        customer_service: CustomerService = Depends(provide_customer_service)
) -> dict:
    """
    Login endpoint authenticates user

    Args:
        form_data: data schema for user login
        fcm_token: token to send push notification on user device
        coach_service: service for interacting with coach profile
        customer_service: service for interacting with customer profile
    Raises:
        400 in case if passed empty fields
        404 if specified user was not found
        400 in case if user is found but credentials are not valid
    Returns:
        access_token and refresh_token inside dictionary
    """
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty fields"
        )

    coach = await coach_service.find({"username": form_data.username})
    customer = await customer_service.find({"username": form_data.username})

    if coach:
        service = coach_service
    elif customer:
        service = customer_service
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any user"
        )

    try:
        user = await service.authorize(form_data, fcm_token)
    except NotValidCredentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not valid credentials for: {form_data.username}"
        )

    return {
        "id": str(user.id),
        "user_type": service.user_type,
        "first_name": user.first_name,
        "access_token": await create_access_token(str(user.username)),
        "refresh_token": await create_refresh_token(str(user.username)),
        "password_changed": bool(password_context.identify(user.password))
    }


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get details of currently logged in user")
async def get_me(
        service: ProfileService = Depends(provide_user_service)
) -> dict:
    """
    Returns short info about current user
    Endpoint can be used by both a coach and a customer

    Args:
        service: service for interacting with profile

    Returns:
        dict: short info about current user
    """
    user = service.user

    return {
        "id": str(user.id),
        "user_type": service.user_type,
        "username": user.username,
        "first_name": user.first_name
    }


@auth_router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileOut,
    summary="Get user profile")
async def get_profile(
        service: ProfileService = Depends(provide_user_service)
) -> dict:
    """
    Returns full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        service: service for interacting with profile

    Returns:
        dict: full info about current user
    """
    user = service.user

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": service.user_type,
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_link": user.photo_path.split('/backend')[1] if user.photo_path else None
    }


@auth_router.post(
    "/profiles",
    summary="Update user profile",
    response_model=UserProfileOut,
    status_code=status.HTTP_200_OK)
async def update_profile(
        service: ProfileService = Depends(provide_user_service),
        first_name: str = Form(...),
        username: str = Form(...),
        last_name: str = Form(None),
        photo: UploadFile = File(None),
        gender: Optional[Gender] = Form(None),
        birthday: date = Form(None),
        email: str = Form(None)
) -> dict:
    """
    Updated full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        service: service for interacting with profile
        first_name: client value from body
        username: client value from body
        last_name: client value from body
        photo: client file from body
        gender: client value from body
        birthday: client value from body
        email: client value from body

    Returns:
        dictionary with updated full user info
    """
    user = service.user

    await service.update(
        first_name=first_name,
        username=username,
        last_name=last_name,
        photo=photo,
        gender=gender,
        birthday=birthday,
        email=email
    )

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": service.user_type,
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_link": user.photo_path.split('/backend')[1] if user.photo_path else None
    }


@auth_router.post(
    "/confirm_password",
    summary="Confirm current user password",
    status_code=status.HTTP_200_OK)
async def confirm_password(
        current_password: str = Form(...),
        service: ProfileService = Depends(provide_user_service)
) -> dict:
    """
    Confirms that user knows current password before it is changed.

    Args:
        current_password: current user password
        service: service for interacting with profile

    Returns:
        success or failed response
    """
    user = service.user

    is_confirmed = await service.confirm_password(current_password)
    if is_confirmed:
        return {"user_id": str(user.id), "confirmed_password": True}
    return {"user_id": str(user.id), "confirmed_password": False}


@auth_router.patch(
    "/change_password",
    summary="Change user password",
    status_code=status.HTTP_200_OK)
async def change_password(
        new_password: NewUserPassword,
        service: ProfileService = Depends(provide_user_service)
) -> dict:
    """
    Changes user password.
    Validation set in schemas.

    Args:
        new_password: new user password
        service: service for interacting with profile

    Returns:
        success response
    """
    user = service.user

    is_changed = await service.update(password=new_password)
    if await is_changed:
        return {"user_id": str(user.id), "changed_password": True}
    return {"user_id": str(user.id), "changed_password": False}
