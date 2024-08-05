from pydantic import BaseModel


class UserLoginData(BaseModel):
    received_password: str
    fcm_token: str


class LoginOut(BaseModel):
    """
    Response after successfully user login
    """
    id: str
    user_type: str
    first_name: str
    access_token: str
    refresh_token: str
    password_changed: bool
