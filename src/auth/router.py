from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import UserRegisterIn, UserRegisterOut, TokenSchema
from src.auth.utils import (
    get_hashed_password, verify_password,
    create_access_token, create_refresh_token
)
from src.auth.dependencies import get_current_user
from src.dependencies import get_db

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterOut)
async def create_user(
        data: UserRegisterIn,
        db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == data.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    user = User(
        username=data.username,
        password=get_hashed_password(data.password)
    )

    db.add(user)
    db.commit()

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
        db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not found"
        )

    hashed_password = user.password
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username)
    }
