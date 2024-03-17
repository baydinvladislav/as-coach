import logging
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src import Customer
from src.schemas.authentication import UserLoginData
from src.schemas.customer import CustomerRegistrationData
from src.utils import verify_password
from src.repository.customer import CustomerRepository
from src.shared.exceptions import NotValidCredentials
from src.service.authentication.user import ProfileService, ProfileType
from src.service.notification import NotificationService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
OTP_LENGTH = 4


# selecting/querying operations
class CustomerSelectorService:

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def provide_by_pk(self, pk: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_pk(pk=pk)

        if customer:
            self.user = customer
            return self.user

    async def provide_customer_by_otp(self, password) -> Customer | None:
        customer = await self.customer_repository.provide_customer_by_otp(password=password)

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


# auth logic
class CustomerProfileService(ProfileService):

    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def register(self, data: CustomerRegistrationData) -> Customer:
        customer = await self.customer_repository.create(
            coach_id=data.coach_id,
            username=data.username,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        logger.info(f"Customer created successfully: {customer.first_name} {customer.last_name}")
        return customer

    async def authorize(self, data: UserLoginData) -> Customer:
        """
        Customer logs in with one time password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.
        """
        first_login = len(data.received_password) == OTP_LENGTH and data.db_password == data.received_password
        regular_login = await verify_password(data.received_password, data.db_password)

        if first_login or regular_login:
            if await self.fcm_token_actualize(data.fcm_token) is False:
                await self.customer_repository.update(data.user_id, fcm_token=data.fcm_token)
            return self.user

        raise NotValidCredentials

    async def update(self, user_id: str, **params) -> None:
        await self.handle_profile_photo(params.pop("photo"))
        await self.customer_repository.update(user_id, **params)


class CustomerService:

    def __init__(
            self,
            profile_service: CustomerProfileService,
            notification_service: NotificationService,
            selector_service: CustomerSelectorService,
    ) -> None:
        self.user: Customer | None = None
        self.user_type = ProfileType.CUSTOMER.value
        self.auth_service = profile_service
        self.notification_service = notification_service
        self.selector_service = selector_service

    async def register_customer(self, data: CustomerRegistrationData) -> Customer:
        customer = await self.auth_service.register(data)
        logger.info(f"Customer registered successfully: {customer.first_name} {customer.last_name}")
        if customer.username is not None:
            logger.info(f"Will be invited in application new customer: {customer.username}")
            await self.notification_service.send_telegram_customer_invite(
                data.coach_name, customer.username, customer.password
            )
            logger.info(f"Customer {customer.username} successfully invited through Telegram account")
        return customer

    async def authorize_customer(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Customer | None:
        if len(form_data.password) == 4:
            self.user = await self.get_customer_by_otp(form_data.password)
            logger.info(f"First customer login {self.user.id}")
        else:
            self.user = await self.get_customer_by_username(form_data.username)
            logger.info(f"Regular customer login {self.user.id}")

        if self.user is None:
            logger.warning(f"Not found any customer in database")
            return None

        try:
            customer = await self.auth_service.authorize(
                UserLoginData(
                    user_id=str(self.user.id),
                    db_password=str(self.user.password),
                    received_password=form_data.password,
                    fcm_token=fcm_token,
                )
            )
            logger.info(f"Customer successfully {customer.last_name} {customer.first_name} login")
            return customer

        except NotValidCredentials:
            logger.warning(f"Not valid credentials for customer")
            return None

    async def update_customer(self, **params) -> Customer | None:
        customer = await self.auth_service.update(user_id=str(self.user.id), photo=params.pop("photo"), **params)
        return customer

    async def get_customer_by_pk(self, pk: str) -> Customer | None:
        customer = await self.selector_service.provide_by_pk(pk=pk)
        return customer

    async def get_customer_by_otp(self, opt: str) -> Customer | None:
        customer = await self.selector_service.provide_customer_by_otp(password=opt)
        return customer

    async def get_customers_by_coach_id(self, coach_id: str) -> list[dict[str, str]]:
        customers = await self.selector_service.get_customers_by_coach_id(coach_id)
        return customers

    async def get_customer_by_username(self, username: str) -> Customer | None:
        customer = await self.selector_service.get_customer_by_username(username)
        return customer

    async def get_customer_by_full_name(self, first_name: str, last_name: str) -> Customer | None:
        customer = await self.selector_service.get_customer_by_full_name(first_name, last_name)
        return customer
