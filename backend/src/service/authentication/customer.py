from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src import Customer
from src.utils import verify_password
from src.repository.customer import CustomerRepository
from src.service.authentication.exceptions import NotValidCredentials
from src.service.authentication.user import UserService, UserType


class CustomerService(UserService):

    def __init__(self, customer_repository: CustomerRepository):
        self.user = None
        self.user_type = UserType.CUSTOMER.value
        self.customer_repository = customer_repository

    async def register(self, coach_id: str, **kwargs) -> Customer:
        customer = await self.customer_repository.create(coach_id=coach_id, **kwargs)
        return customer

    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Customer:
        """
        Customer logs in with default password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.

        Args:
            form_data: customer credentials passed by client
            fcm_token: token to send push notification on user device

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        password_in_db = str(self.user.password)
        if password_in_db == form_data.password \
                or await verify_password(form_data.password, password_in_db):

            # to update User.fcm_token
            if self.user.fcm_token != fcm_token:
                await self.set_fcm_token(fcm_token)
                await self.customer_repository.update(str(self.user.id), fcm_token=fcm_token)

            return self.user

        raise NotValidCredentials

    async def update(self, **params) -> None:
        await self.handle_profile_photo(params.pop("photo"))
        await self.customer_repository.update(str(self.user.id), **params)

    async def get_customer_by_pk(self, pk: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_pk(pk=pk)

        if customer:
            self.user = customer
            return self.user

    async def get_customers_by_coach_id(self, coach_id: str) -> list[dict[str, str]]:
        customers_aggregates = await self.customer_repository.provide_customers_by_coach_id(coach_id)

        customers = []
        archive_customers = []
        for customer in customers_aggregates:
            last_plan_end_date = customer[4]

            if last_plan_end_date and datetime.now().date() - last_plan_end_date > timedelta(days=30):
                archive_customers.append({
                    "id": str(customer[0]),
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "phone_number": customer[3],
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d")
                })
            else:
                customers.append({
                    "id": str(customer[0]),
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "phone_number": customer[3],
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d") if last_plan_end_date else None
                })

        customers.extend(archive_customers)
        return customers

    async def get_customer_by_username(self, username: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_username(username)

        if customer:
            self.user = customer[0]
            return self.user

    async def get_customer_by_full_name(self, first_name: str, last_name: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_full_name(first_name, last_name)

        if customer:
            self.user = customer[0]
            return self.user

    # deprecating...
    async def find(self, filters: dict) -> Optional[Customer]:
        foreign_keys, sub_queries = ["training_plans"], ["trainings", "diets"]
        customer = await self.customer_repository.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if customer:
            self.user = customer[0]
            return self.user
