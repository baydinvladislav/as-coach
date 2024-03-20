import logging
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src import Customer
from src.shared.config import OTP_LENGTH
from src.schemas.authentication import CustomerRegistrationData, UserLoginData
from src.service.notification import NotificationService
from src.utils import verify_password
from src.repository.customer import CustomerRepository
from src.service.user import UserService, UserType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# TODO form Customer aggregate in this layer
class CustomerSelectorService:

    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def select_customer_by_pk(self, pk: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_pk(pk=pk)
        return customer

    async def select_customer_by_otp(self, password) -> Customer | None:
        customer = await self.customer_repository.provide_by_otp(password=password)
        return customer

    async def select_customers_by_coach_id(self, coach_id: str) -> list[dict[str, str]]:
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

    async def select_customer_by_username(self, username: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_username(username)
        return customer

    async def select_customer_by_full_name(self, first_name: str, last_name: str) -> Customer | None:
        customer = await self.customer_repository.provide_by_full_name(first_name, last_name)
        return customer


# TODO form Customer aggregate in this layer
class CustomerProfileService(UserService):
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def register(self, data: CustomerRegistrationData) -> Customer | None:
        customer = await self.customer_repository.create(
            coach_id=data.coach_id,
            username=data.username,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        if customer is None:
            logger.warning(f"New customer creation is failed: {data.last_name} {data.first_name}")
            raise

        logger.info(f"Customer created successfully: {data.last_name} {data.first_name}")
        return customer

    async def authorize(self, user: Customer, data: UserLoginData) -> bool:
        """
        Customer logs in with one time password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.
        """
        first_login = len(data.received_password) == OTP_LENGTH and user.password == data.received_password
        regular_login = await verify_password(data.received_password, user.password)

        if first_login or regular_login:
            if await self.fcm_token_actualize(user, data.fcm_token) is False:
                await self.customer_repository.update(str(user.id), fcm_token=data.fcm_token)
            return True
        return False

    async def update(self, user: Customer, **params) -> None:
        if "photo" in params:
            await self.handle_profile_photo(user, params.pop("photo"))
        await self.customer_repository.update(str(user.id), **params)


class CustomerService:

    def __init__(
            self,
            selector_service: CustomerSelectorService,
            profile_service: CustomerProfileService,
            notification_service: NotificationService,
    ) -> None:
        self.user = None
        self.user_type = UserType.CUSTOMER.value
        self.selector_service = selector_service
        self.profile_service = profile_service
        self.notification_service = notification_service

    async def register(self, data: CustomerRegistrationData) -> Customer:
        customer = await self.profile_service.register(data)
        logger.info(f"Customer registered successfully: {customer.first_name} {customer.last_name}")
        if customer.username is not None:
            logger.info(f"Will be invited in application new customer: {customer.username}")
            await self.notification_service.send_telegram_customer_invite(
                data.coach_name, customer.username, customer.password
            )
            logger.info(f"Customer {customer.username} successfully invited through Telegram account")
        return customer

    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Customer | None:
        """
        Customer logs in with default password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.

        Args:
            form_data: customer credentials passed by client
            fcm_token: token to send push notification on user device

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        if len(form_data.password) == OTP_LENGTH:
            self.user = await self.get_customer_by_otp(form_data.password)
        else:
            self.user = await self.get_customer_by_username(form_data.username)

        if self.user is None:
            logger.warning(f"Not found any customer in database")
            return None

        data = UserLoginData(received_password=form_data.password, fcm_token=fcm_token)
        if await self.profile_service.authorize(self.user, data) is True:
            await self.update(self.user, username=form_data.username)
            logger.info(f"Customer successfully {self.user.last_name} {self.user.first_name} login")
            return self.user

        return None

    async def confirm_password(self, user: Customer, current_password: str) -> bool:
        if await self.profile_service.confirm_password(user, current_password):
            return True
        return False

    async def update(self, user: Customer, **params) -> None:
        await self.profile_service.update(user, **params)

    async def get_customer_by_pk(self, pk: str) -> Customer | None:
        customer = await self.selector_service.select_customer_by_pk(pk=pk)
        if customer is not None:
            self.user = customer
            return self.user
        return None

    async def get_customer_by_otp(self, otp: str) -> Customer | None:
        customer = await self.selector_service.select_customer_by_otp(password=otp)
        if customer:
            self.user = customer
            return self.user
        return None

    async def get_customers_by_coach_id(self, coach_id: str) -> list[dict[str, str]]:
        customers = await self.selector_service.select_customers_by_coach_id(coach_id)
        return customers

    async def get_customer_by_username(self, username: str) -> Customer | None:
        customer = await self.selector_service.select_customer_by_username(username)
        if customer is not None:
            self.user = customer[0]
            return self.user
        return None

    async def get_customer_by_full_name(self, first_name: str, last_name: str) -> Customer | None:
        customer = await self.selector_service.select_customer_by_full_name(first_name, last_name)
        if customer is not None:
            self.user = customer[0]
            return self.user
        return None
