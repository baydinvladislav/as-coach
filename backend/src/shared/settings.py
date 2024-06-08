import os
from dataclasses import dataclass

from fastapi.security import OAuth2PasswordBearer


@dataclass
class InfrastructureSettings:
    database_url: str = os.environ.get("DATABASE_URL")
    static_dir: str = os.path.join(os.getcwd(), "static")


@dataclass
class AuthSettings:
    access_token_expire_minutes: str = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: str = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")
    algorithm: str = os.environ.get("ALGORITHM")
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.environ.get("JWT_REFRESH_SECRET_KEY")
    # original spelling TODO: fix it
    reuseable_oauth: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/login", scheme_name="JWT")
    otp_length: int = 4


@dataclass
class FirebaseSettings:
    firebase_type = os.environ.get("FIREBASE_TYPE", "")
    firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID", "")
    firebase_private_key_id = os.environ.get("FIREBASE_PRIVATE_KEY_ID", "")
    firebase_private_key = os.environ.get("FIREBASE_PRIVATE_KEY", "")
    firebase_client_email = os.environ.get("FIREBASE_CLIENT_EMAIL", "")
    firebase_client_id = os.environ.get("FIREBASE_CLIENT_ID", "")
    firebase_auth_uri = os.environ.get("FIREBASE_AUTH_URI", "")
    firebase_token_uri = os.environ.get("FIREBASE_TOKEN_URI", "")
    firebase_auth_provider_cert_url = os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL", "")
    firebase_client_cert_url = os.environ.get("FIREBASE_CLIENT_CERT_URL", "")
    firebase_universe_domain = os.environ.get("FIREBASE_UNIVERSE_DOMAIN", "")


@dataclass
class TestingSettings:
    test_env = os.environ.get("TEST_ENV", 0)
    test_database_url = os.environ.get("TEST_DATABASE_URL")
    test_coach_first_name = os.getenv("TEST_COACH_FIRST_NAME")
    test_coach_last_name = os.getenv("TEST_COACH_LAST_NAME")
    test_coach_username = os.getenv("TEST_COACH_USERNAME")
    test_coach_password = os.getenv("TEST_COACH_PASSWORD")
    test_customer_first_name = os.getenv("TEST_CUSTOMER_FIRST_NAME")
    test_customer_last_name = os.getenv("TEST_CUSTOMER_LAST_NAME")
    test_customer_username = os.getenv("TEST_CUSTOMER_USERNAME")


@dataclass
class AppSettings:
    infrastructure_settings: InfrastructureSettings
    auth_settings: AuthSettings
    firebase_settings: FirebaseSettings
    testing_settings: TestingSettings
