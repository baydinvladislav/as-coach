from fastapi.security import OAuth2PasswordRequestForm

from src.core.services.exceptions import UserDoesNotExist
from src.infrastructure.schemas.auth import CoachRegisterIn


class ProfileService:

    def __init__(self, coach_service, customer_service):
        self.coach_service = coach_service
        self.customer_service = customer_service

    async def authorize_user(self, form_data: OAuth2PasswordRequestForm):
        found_roles_by_username = await self.get_me(form_data.username)
        coach, customer = found_roles_by_username["coach"], found_roles_by_username["customer"]

        if coach:
            await self.coach_service.authorize_coach(coach, form_data.password)
            return coach
        elif customer:
            await self.customer_service.authorize_customer(customer, form_data.password)
            return customer
        else:
            raise UserDoesNotExist

    async def register_user(self, data: CoachRegisterIn):
        coach = await self.coach_service.register_coach(data)
        return coach

    async def get_me(self, username) -> dict:
        coach = await self.coach_service.find_coach_by_username(username)
        customer = await self.customer_service.find_customer_by_username(username)
        return {"coach": coach, "customer": customer}

    async def get_current_user(self, username):
        cur_user: dict = await self.get_me(username)
        user = cur_user["coach"] or cur_user["customer"]

        if user is None:
            raise UserDoesNotExist

        return user
