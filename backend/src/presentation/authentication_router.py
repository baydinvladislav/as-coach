from datetime import date
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.coach_service import CoachService
from src.service.customer_service import CustomerService
from src.shared.exceptions import UsernameIsTaken, NotValidCredentials
from src.shared.dependencies import (
    provide_database_unit_of_work,
    provide_user_service,
    provide_coach_service,
    provide_customer_service,
)
from src.persistence.models import Gender
from src.presentation.schemas.profile_schema import (
    UserProfileOut,
    NewUserPassword,
    CurrentUserOut,
)
from src.presentation.schemas.login_schema import LoginOut
from src.presentation.schemas.register import CoachRegistrationData, UserRegisterOut
from src.utils import password_context, get_hashed_password

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Creates new coach",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut)
async def register_coach(
    coach_data: CoachRegistrationData,
    coach_service: CoachService = Depends(provide_coach_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> UserRegisterOut:
    try:
        coach = await coach_service.register_coach(uow, coach_data)
    except UsernameIsTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Coach with phone number: {coach_data.username} already exists"
        )
    return UserRegisterOut(
        id=str(coach.id),
        first_name=coach.first_name,
        username=coach.username,
        access_token=await coach_service.profile_service.generate_jwt_token(coach.username, access=True),
        refresh_token=await coach_service.profile_service.generate_jwt_token(coach.username, refresh=True),
    )


@auth_router.post(
    "/login",
    summary="Authorizes any user, both trainer and customer",
    status_code=status.HTTP_200_OK,
    response_model=LoginOut)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    fcm_token: str = Form(...),
    coach_service: CoachService = Depends(provide_coach_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> LoginOut:
    """
    Login endpoint authenticates user

    Args:
        form_data: data schema for user login
        fcm_token: token to send push notification on user device
        coach_service: service for interacting with coach profile
        customer_service: service for interacting with customer profile
        uow: db session injection
    Raises:
        400 in case if passed empty fields
        404 if specified user was not found
        400 in case if user is found but credentials are not valid
    Returns:
        access_token and refresh_token inside dictionary
    """
    if form_data.username is None or form_data.password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty credential fields")

    try:
        coach = await coach_service.authorize_coach(
            uow=uow,
            form_data=form_data,
            fcm_token=fcm_token,
        )
    except NotValidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not valid credentials for coach")

    if coach is not None:
        user, service = coach, coach_service
    else:
        try:
            customer = await customer_service.authorize(
                uow=uow,
                form_data=form_data,
                fcm_token=fcm_token,
            )
        except NotValidCredentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not valid credentials for customer")

        if customer is not None:
            user, service = customer, customer_service
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found any user")

    return LoginOut(
        id=str(user.id),
        user_type=service.user_type,
        first_name=user.first_name,
        access_token=await service.profile_service.generate_jwt_token(user.username, access=True),
        refresh_token=await service.profile_service.generate_jwt_token(user.username, refresh=True),
        password_changed=bool(password_context.identify(user.password)),
    )


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=CurrentUserOut,
    summary="Get details of currently logged in user")
async def get_me(
    service: CoachService | CustomerService = Depends(provide_user_service),
) -> CurrentUserOut:
    """
    Returns short info about current user
    Endpoint can be used by both a coach and a customer

    Args:
        service: service for interacting with profile

    Returns:
        dict: short info about current user
    """
    user = service.user

    return CurrentUserOut(
        id=str(user.id),
        user_type=service.user_type,
        username=user.username,
        first_name=user.first_name,
    )


@auth_router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileOut,
    summary="Get user profile")
async def get_profile(
    service: CoachService | CustomerService = Depends(provide_user_service),
) -> UserProfileOut:
    """
    Returns full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        service: service for interacting with profile

    Returns:
        dict: full info about current user
    """
    user = service.user

    return UserProfileOut(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        user_type=service.user_type,
        birthday=user.birthday,
        email=user.email,
        username=user.username,
        photo_link=user.photo_link.split('/backend')[1] if user.photo_link else None,
    )


@auth_router.post(
    "/profiles",
    summary="Update user profile",
    response_model=UserProfileOut,
    status_code=status.HTTP_200_OK)
async def update_profile(
    service: CoachService | CustomerService = Depends(provide_user_service),
    first_name: str = Form(...),
    username: str = Form(...),
    last_name: str = Form(None),
    photo: UploadFile = File(None),
    gender: Optional[Gender] = Form(None),
    birthday: date = Form(None),
    email: str = Form(None),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> UserProfileOut:
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
        uow: db session injection

    Returns:
        dictionary with updated full user info
    """
    user = service.user

    updated_user = await service.update_profile(
        uow=uow,
        user=user,
        password=user.password,
        fcm_token=user.fcm_token,
        first_name=first_name,
        username=username,
        last_name=last_name,
        photo=photo,
        gender=gender,
        birthday=birthday,
        email=email,
    )

    return UserProfileOut(
        id=str(updated_user.id),
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        user_type=service.user_type,
        gender=updated_user.gender,
        birthday=updated_user.birthday,
        email=updated_user.email,
        username=updated_user.username,
        photo_link=user.photo_link.split('/backend')[1] if user.photo_link else None,
    )


@auth_router.delete(
    "/profiles",
    summary="Delete user profile",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    uow: AsyncSession = Depends(provide_database_unit_of_work),
    service: CoachService | CustomerService = Depends(provide_user_service),
):
    user = service.user
    await service.delete(uow, user)
    return None


@auth_router.post(
    "/confirm_password",
    summary="Confirm current user password",
    status_code=status.HTTP_200_OK)
async def confirm_password(
    current_password: str = Form(...),
    service: CoachService | CustomerService = Depends(provide_user_service)
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

    is_confirmed = await service.confirm_coach_password(user, current_password)
    if is_confirmed:
        return {"user_id": str(user.id), "confirmed_password": True}
    return {"user_id": str(user.id), "confirmed_password": False}


@auth_router.patch(
    "/change_password",
    summary="Change user password",
    status_code=status.HTTP_200_OK)
async def change_password(
    new_password: NewUserPassword,
    uow: AsyncSession = Depends(provide_database_unit_of_work),
    service: CoachService | CustomerService = Depends(provide_user_service),
) -> dict:
    user = service.user
    await service.update_profile(
        uow=uow,
        user=user,
        password=await get_hashed_password(new_password.password)
    )
    return {"user_id": str(user.id), "changed_password": True}
