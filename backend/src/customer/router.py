from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.customer.schemas import CustomerCreateIn, CustomerCreateOut
from src.dependencies import get_db
from src.auth.dependencies import get_current_user
from src.customer.models import Customer

customer_router = APIRouter()


@customer_router.post(
    "/customers",
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerCreateOut)
async def create_user(
        customer_data: CustomerCreateIn,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)):
    """
    Creates new customer for user

    Args:
        customer_data: data to create new customer
        database: dependency injection for access to database
        current_user: returns current application user
    Raises:
        400 in case if customer with the phone number already created
    Returns:
        dictionary with just created user, id and username as keys
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
