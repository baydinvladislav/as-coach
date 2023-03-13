from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    username: str
    password: str


class UserRegisterOut(BaseModel):
    id: str
    username: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
