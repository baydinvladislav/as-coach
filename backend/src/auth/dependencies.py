"""
Dependencies for auth service
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.models import User
from src.dependencies import get_db
from src.auth.utils import decode_jwt_token

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)):
    """
    Provide endpoint permission only for coach

    Extracts username from client token,
    provides current user
    """
    token_data = decode_jwt_token(token)
    token_username = token_data.sub

    user = database.query(User).filter(User.username == token_username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    return user
