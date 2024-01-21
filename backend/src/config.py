"""
Common application config
"""

import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

# TODO: let's check that .env file on the place

# load environment variables from the .env file
load_dotenv()

# infrastructure
DATABASE_URL = os.environ.get("DATABASE_URL")
STATIC_DIR = os.path.join(os.getcwd(), "static")

# testing
TEST_ENV = os.environ.get("TEST_ENV", 0)
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
TEST_COACH_FIRST_NAME = os.getenv("TEST_COACH_FIRST_NAME")
TEST_COACH_LAST_NAME = os.getenv("TEST_COACH_LAST_NAME")
TEST_COACH_USERNAME = os.getenv("TEST_COACH_USERNAME")
TEST_COACH_PASSWORD = os.getenv("TEST_COACH_PASSWORD")
TEST_CUSTOMER_FIRST_NAME = os.getenv("TEST_CUSTOMER_FIRST_NAME")
TEST_CUSTOMER_LAST_NAME = os.getenv("TEST_CUSTOMER_LAST_NAME")
TEST_CUSTOMER_USERNAME = os.getenv("TEST_CUSTOMER_USERNAME")

# auth
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.environ.get("ALGORITHM")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)

# firebase push notifications
FIREBASE_TYPE = os.environ.get("FIREBASE_TYPE", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_PRIVATE_KEY_ID = os.environ.get("FIREBASE_PRIVATE_KEY_ID", "")
FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY", "")
FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL", "")
FIREBASE_CLIENT_ID = os.environ.get("FIREBASE_CLIENT_ID", "")
FIREBASE_AUTH_URI = os.environ.get("FIREBASE_AUTH_URI", "")
FIREBASE_TOKEN_URI = os.environ.get("FIREBASE_TOKEN_URI", "")
FIREBASE_AUTH_PROVIDER_CERT_URL = os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL", "")
FIREBASE_CLIENT_CERT_URL = os.environ.get("FIREBASE_CLIENT_CERT_URL", "")
FIREBASE_UNIVERSE_DOMAIN = os.environ.get("FIREBASE_UNIVERSE_DOMAIN", "")
