from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import UserAuth, UserOut, TokenSchema
from src.auth.utils import (
    get_hashed_password, verify_password,
    create_access_token, create_refresh_token
)
from src.dependencies import get_db

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut)
async def create_user(
        data: UserAuth,
        db: Session = Depends(get_db)):

    user = db.query(User).get(data.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    user = User(
        username=data.username,
        password=get_hashed_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        gender=data.gender
    )

    db.add(user)
    db.commit()

    return user


@auth_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):

    user = db.query(User).get(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_password = user.password
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username)
    }
