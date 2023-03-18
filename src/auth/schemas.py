from pydantic import BaseModel, validator


class UserRegisterIn(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_phone_number(cls, value):
        """
        We have to get: +79xxxxxxxxx
        Phone number contains 9 numbers
        """
        if value.startswith("+7") and len(value) == 9:
            return value
        raise ValueError("Specify correct phone number")

    @validator("password")
    def validate_password(cls, value):
        if 8 <= len(value) <= 128:
            return value
        raise ValueError("Password must be greater than 7 symbols and less than 129 symbols")


class UserRegisterOut(BaseModel):
    id: str
    username: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
