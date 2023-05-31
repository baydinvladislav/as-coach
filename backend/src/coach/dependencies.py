"""
Dependencies for customer service triggered
during request to only for coach API endpoints
"""

from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.coach.models import Coach
from src.dependencies import get_db
from src.auth.utils import decode_jwt_token

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_current_coach(
        token: str = Depends(reuseable_oauth),
        database: Session = Depends(get_db)
) -> Union[Coach, None]:
    """
    Provides current coach during request to only coach's API endpoints

    Args:
        token: jwt token which contains user username
        database: dependency injection for access to database

    Return:
        coach: Coach ORM obj or None if coach wasn't found
    """
    token_data = decode_jwt_token(token)
    token_username = token_data.sub
    coach = database.query(Coach).filter(Coach.username == token_username).first()
    return coach
