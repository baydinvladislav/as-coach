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

from src.core.usecases.coach_usecase import CoachUseCase
from src.core.usecases.customer_usecase import CustomerUseCase
from src.core.usecases.profile_usecase import ProfileUseCase
from src.core.usecases.exceptions import NotValidCredentials, UsernameIsTaken
from src.dependencies import define_user_use_case, provide_coach_use_case, provide_customer_use_case
from src.models import Gender
from src.interfaces.schemas.auth import (
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
        use_case: CoachUseCase = Depends(provide_coach_use_case)
) -> dict:
    """
    Registration endpoint, creates new user in database.
    Registration for customers implemented through adding coach's invites.

    Args:
        user_data: data schema for user registration
        use_case: service for interacting with profile
    Raises:
        400 in case if user with the phone number already created
    Returns:
        dictionary with just created user
    """
    try:
        user = await use_case.register(user_data)
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
        coach_use_case: CoachUseCase = Depends(provide_coach_use_case),
        customer_use_case: CustomerUseCase = Depends(provide_customer_use_case)
) -> dict:
    """
    Login endpoint authenticates user

    Args:
        form_data: data schema for user login
        coach_use_case: service for interacting with coach profile
        customer_use_case: service for interacting with customer profile
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

    coach = await coach_use_case.find({"username": form_data.username})
    customer = await customer_use_case.find({"username": form_data.username})

    if coach:
        service = coach_use_case
    elif customer:
        service = customer_use_case
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any user"
        )

    try:
        user = await service.authorize(form_data)
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
        use_case: ProfileUseCase = Depends(define_user_use_case)
) -> dict:
    """
    Returns short info about current user
    Endpoint can be used by both a coach and a customer

    Args:
        use_case: service for interacting with profile

    Returns:
        dict: short info about current user
    """
    user = use_case.user

    return {
        "id": str(user.id),
        "user_type": use_case.user_type,
        "username": user.username,
        "first_name": user.first_name
    }


@auth_router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileOut,
    summary="Get user profile")
async def get_profile(
        use_case: ProfileUseCase = Depends(define_user_use_case)
) -> dict:
    """
    Returns full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        use_case: service for interacting with profile

    Returns:
        dict: full info about current user
    """
    user = use_case.user

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": use_case.user_type,
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
        use_case: ProfileUseCase = Depends(define_user_use_case),
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
        use_case: service for interacting with profile
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
    user = use_case.user

    await use_case.update(
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
        "user_type": use_case.user_type,
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
        use_case: ProfileUseCase = Depends(define_user_use_case)
) -> dict:
    """
    Confirms that user knows current password before it is changed.

    Args:
        current_password: current user password
        use_case: service for interacting with profile

    Returns:
        success or failed response
    """
    user = use_case.user

    is_confirmed = await use_case.confirm_password(current_password)
    if is_confirmed:
        return {"user_id": str(user.id), "confirmed_password": True}
    return {"user_id": str(user.id), "confirmed_password": False}


@auth_router.patch(
    "/change_password",
    summary="Change user password",
    status_code=status.HTTP_200_OK)
async def change_password(
        new_password: NewUserPassword,
        use_case: ProfileUseCase = Depends(define_user_use_case)
) -> dict:
    """
    Changes user password.
    Validation set in schemas.

    Args:
        new_password: new user password
        use_case: service for interacting with profile

    Returns:
        success response
    """
    user = use_case.user

    is_changed = await use_case.update(password=new_password)
    if await is_changed:
        return {"user_id": str(user.id), "changed_password": True}
    return {"user_id": str(user.id), "changed_password": False}
