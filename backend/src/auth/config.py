"""
Auth service config
"""

import os
from fastapi.security import OAuth2PasswordBearer


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.environ.get("ALGORITHM")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
