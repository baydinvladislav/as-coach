import logging
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src import Customer
from src.schemas.customer_schema import CustomerOut
from src.shared.config import OTP_LENGTH
from src.schemas.authentication_schema import CustomerRegistrationData, UserLoginData
from src.schemas.user_coach_schema import UserCustomerSchema
from src.service.notification_service import NotificationService
from src.shared.exceptions import NotValidCredentials
from src.utils import verify_password
from src.repository.customer_repository import CustomerRepository
from src.service.user_service import UserService, UserType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CustomerSelectorService:
    """Responsible for getting customer data from storage"""

    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def select_customer_by_pk(self, uow: Session, pk: str) -> UserCustomerSchema | None:
        customer = await self.customer_repository.provide_by_pk(uow, pk=pk)
        return customer

    async def select_customer_by_otp(self, uow: Session, password) -> UserCustomerSchema | None:
        customer = await self.customer_repository.provide_by_otp(uow, password=password)
        return customer

    async def select_customers_by_coach_id(self, uow: Session, coach_id: str) -> list[dict[str, str]]:
        customers_aggregates = await self.customer_repository.provide_customers_by_coach_id(uow, coach_id)

        customers = []
        archive_customers = []
        for customer in customers_aggregates:
            last_plan_end_date = customer.last_plan_end_date

            if last_plan_end_date and datetime.now().date() - last_plan_end_date > timedelta(days=30):
                archive_customers.append({
                    "id": str(customer.id),
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.username,
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d")
                })
            else:
                customers.append({
                    "id": str(customer.id),
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.username,
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d") if last_plan_end_date else None
                })

        customers.extend(archive_customers)
        return customers

    async def select_customer_by_username(self, uow: Session, username: str) -> UserCustomerSchema | None:
        customer = await self.customer_repository.provide_by_username(uow, username)
        return customer

    async def select_customer_by_full_name(
        self, uow: Session, coach_id: str, first_name: str, last_name: str
    ) -> UserCustomerSchema | None:
        customer = await self.customer_repository.provide_by_coach_id_and_full_name(
            uow=uow,
            coach_id=coach_id,
            first_name=first_name,
            last_name=last_name,
        )
        return customer


class CustomerProfileService(UserService):
    """Responsible for customer profile operations"""

    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def register_user(self, uow: Session, data: CustomerRegistrationData) -> UserCustomerSchema | None:
        customer = await self.customer_repository.create_customer(uow, data)

        if customer is None:
            logger.warning(f"New customer creation is failed: {data.last_name} {data.first_name}")
            raise

        logger.info(f"Customer created successfully: {data.last_name} {data.first_name}")
        return customer

    async def authorize_user(self, uow: Session, user: Customer, data: UserLoginData) -> bool:
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

    async def update_user_profile(self, uow: Session, user: Customer, **params) -> None:
        if "photo" in params:
            await self.handle_profile_photo(user, params.pop("photo"))
        await self.customer_repository.update_customer(uow, id=str(user.id), **params)

    async def delete(self, uow: Session, user: Customer) -> str | None:
        deleted_id = await self.customer_repository.delete_customer(uow, str(user.id))
        return deleted_id


class CustomerService:
    """Contains business rules for Customer subdomain"""

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

    async def register(self, uow: Session, data: CustomerRegistrationData) -> UserCustomerSchema:
        customer = await self.profile_service.register_user(uow, data)
        logger.info(f"Customer registered successfully: {customer.first_name} {customer.last_name}")
        uow.commit()

        if customer.telegram_username is not None:
            logger.info(f"Will be invited in application new customer: {customer.telegram_username}")
            # pass write_uow to use outbox service
            await self.notification_service.send_telegram_customer_invite(
                coach_name=data.coach_name,
                customer_username=customer.telegram_username,
                customer_password=customer.password,
            )
            logger.info(f"Customer {customer.telegram_username} successfully invited through Telegram account")

        return customer

    async def authorize(
        self, uow: Session, form_data: OAuth2PasswordRequestForm, fcm_token: str
    ) -> UserCustomerSchema | None:
        """
        Customer logs in with default password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.

        Args:
            uow: db session
            form_data: customer credentials passed by client
            fcm_token: token to send push notification on user device

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        if len(form_data.password) == OTP_LENGTH:
            self.user = await self.get_customer_by_otp(uow, form_data.password)
        else:
            self.user = await self.get_customer_by_username(uow, form_data.username)

        if self.user is None:
            logger.warning(f"Not found any customer in database")
            return None

        data = UserLoginData(received_password=form_data.password, fcm_token=fcm_token)
        if await self.profile_service.authorize_user(uow, self.user, data) is True:
            if self.user.username is None:
                await self.update_profile(uow, self.user, username=form_data.username)
            logger.info(f"Customer successfully {self.user.last_name} {self.user.first_name} login")
            return self.user
        raise NotValidCredentials("Not correct customer password")

    async def confirm_password(self, user: Customer, current_password: str) -> bool:
        if await self.profile_service.confirm_password(user, current_password):
            return True
        return False

    async def update_profile(self, uow: Session, user: Customer, **params) -> None:
        await self.profile_service.update_user_profile(uow, user, **params)

    async def delete(self, uow: Session, user: Customer) -> None:
        deleted_id = await self.profile_service.delete(uow, user)
        if deleted_id is None:
            logger.info(f"Couldn't delete customer {user.username}")
            return
        logger.info(f"Customer {user.username} successfully deleted")

    async def get_customer_by_pk(self, uow: Session, pk: str) -> UserCustomerSchema | None:
        customer = await self.selector_service.select_customer_by_pk(uow, pk=pk)
        if customer is not None:
            self.user = customer
            return self.user
        return None

    async def get_customer_by_otp(self, uow: Session, otp: str) -> UserCustomerSchema | None:
        customer = await self.selector_service.select_customer_by_otp(uow, password=otp)
        if customer:
            self.user = customer
            return self.user
        return None

    async def get_customers_by_coach_id(self, uow: Session, coach_id: str) -> list[dict[str, str]]:
        customers = await self.selector_service.select_customers_by_coach_id(uow, coach_id)
        return customers

    async def get_customer_by_username(self, uow: Session, username: str) -> UserCustomerSchema | None:
        customer = await self.selector_service.select_customer_by_username(uow, username)
        if customer is not None:
            self.user = customer[0]
            return self.user
        return None

    async def get_customer_by_full_name_for_coach(
        self, uow: Session, coach_id: str, first_name: str, last_name: str
    ) -> UserCustomerSchema | None:
        customer = await self.selector_service.select_customer_by_full_name(
            uow=uow,
            coach_id=coach_id,
            first_name=first_name,
            last_name=last_name,
        )
        if customer is not None:
            self.user = customer[0]
            return self.user
        return None
