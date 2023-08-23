from fastapi.security import OAuth2PasswordRequestForm

from src.infrastructure.schemas.auth import CoachRegisterIn


class UserDoesNotExist(Exception):
    """
    Raises when user not found
    """
    pass


class NotValidPassword(Exception):
    """
    Raises when passed not valid password
    """
    pass


class UsernameIsTaken(Exception):
    """
    Raises when user is trying to register with busy username
    """
    pass


class ProfileService:

    def __init__(self, coach_service, customer_service):
        self.coach_service = coach_service
        self.customer_service = customer_service

    async def authorize_user(self, form_data: OAuth2PasswordRequestForm):
        coach = await self.coach_service.find_coach_by_username(form_data.username)
        customer = await self.customer_service.find_customer_by_username(form_data.username)

        if not coach and not customer:
            raise UserDoesNotExist

        if coach:
            await self.coach_service.authorize_coach(coach, form_data.password)
            return coach, "coach"
        else:
            await self.customer_service.authorize_customer(customer, form_data.password)
            return customer, "customer"

    async def register_user(self, data: CoachRegisterIn):
        coach = await self.coach_service.register_coach(data)
        return coach
