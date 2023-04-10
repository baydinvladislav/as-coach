from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.customer.schemas import CustomerCreateIn, CustomerOut, TrainingPlanIn, TrainingPlanOut
from src.dependencies import get_db
from src.auth.dependencies import get_current_user
from src.customer.models import Customer
from src.utils import validate_uuid

customer_router = APIRouter()


@customer_router.post(
    "/customers",
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerOut)
async def create_customer(
        customer_data: CustomerCreateIn,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> dict:
    """
    Creates new customer for user

    Args:
        customer_data: data to create new customer
        database: dependency injection for access to database
        current_user: returns current application user
    Raises:
        400 in case if customer with the phone number already created
        400 in case if couple last name and first name already exist
    Returns:
        dictionary with just created customer
        id, first_name, last_name and phone_number are keys
    """
    if customer_data.phone_number:
        customer = database.query(Customer).filter(
            Customer.phone_number == customer_data.phone_number
        ).first()

        if customer is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer {customer.first_name} {customer.last_name} "
                       f"with this phone number already exists."
            )

    if database.query(Customer).filter(
        Customer.first_name == customer_data.first_name,
        Customer.last_name == customer_data.last_name
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer full name: {customer_data.first_name} "
                   f"{customer_data.last_name} already exists."
        )

    customer = Customer(
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        phone_number=customer_data.phone_number,
        user_id=str(current_user.id)
    )

    database.add(customer)
    database.commit()

    return {
        "id": str(customer.id),
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.phone_number
    }


@customer_router.get(
    "/customers",
    summary="Gets all user's customers",
    status_code=status.HTTP_200_OK)
async def get_customers(
        current_user: Session = Depends(get_current_user)
) -> list[Optional[CustomerOut]]:
    """
    Gets all customer for current user

    Args:
        current_user: returns current application user

    Returns:
        list of customers
    """
    customers = []

    for customer in current_user.customers:
        customers.append({
            "id": str(customer.id),
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number
        })

    return customers


@customer_router.get(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK)
async def get_customer(
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)
) -> CustomerOut:
    """
    Gets specific customer by ID.

    Args:
        customer_id: str(UUID) of specified customer.
        database: dependency injection for access to database.
        current_user: returns current application user

    Raise:
        HTTPException: 400 when passed is not correct UUID as customer_id.
        HTTPException: 404 when customer not found.
        HTTPException: 400 when specified customer does not belong to the current user.
    """
    if not validate_uuid(customer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passed customer_id is not correct UUID value"
        )

    customer = database.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )

    if str(customer.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The client belong to another user"
        )

    return {
        "id": str(customer.id),
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.phone_number
    }


@customer_router.post(
    "/customers/{customer_id}/week_plans/",
    summary="Create new training plan for customer",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingPlanOut)
async def create_training_plan(
        training_plan_data: TrainingPlanIn,
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> dict:
    """
    Creates new week plan for specific customer

    Args:
        training_plan_data: data from application user to create new week plan
        customer_id: customer's str(UUID)
        database: dependency injection for access to database
        current_user: dependency injection to define a current user
    """
    pass
