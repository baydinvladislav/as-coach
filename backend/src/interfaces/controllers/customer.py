from typing import Union, Any, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.core.usecases.coach_usecase import CoachUseCase
from src.core.usecases.customer_usecase import CustomerUseCase
from src.core.usecases.trainingplan_usecase import TrainingPlanUseCase
from src.interfaces.schemas.customer import (
    CustomerOut,
    CustomerCreateIn,
    TrainingPlanOut,
    TrainingPlanIn,
    TrainingPlanOutFull
)
from src.dependencies import provide_customer_use_case, define_user_use_case, provide_training_plan_use_case
from src.utils import validate_uuid, generate_random_password

customer_router = APIRouter()


@customer_router.post(
    "/customers",
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerOut)
async def create_customer(
        customer_data: CustomerCreateIn,
        user_use_case: CoachUseCase = Depends(define_user_use_case),
        customer_use_case: CustomerUseCase = Depends(provide_customer_use_case)
) -> dict:
    """
    Creates new customer for coach

    Args:
        customer_data: data to create new customer
        user_use_case: service for interacting with profile
        customer_use_case: service for interacting with customer
    Raises:
        400 in case if customer with the phone number already created
        400 in case if couple last name and first name already exist
    Returns:
        dictionary with just created customer
        id, first_name, last_name and phone_number are keys
    """
    user = user_use_case.user

    customer_in_db = await customer_use_case.find({"username": customer_data.phone_number})
    if customer_data.phone_number and customer_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer {customer_in_db.first_name} {customer_in_db.last_name} "
                   f"with this phone number already exists."
        )

    customer_in_db = await customer_use_case.find(
        {
            "first_name": customer_data.first_name,
            "last_name": customer_data.last_name
        }
    )
    if customer_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer full name: {customer_data.first_name} "
                   f"{customer_data.last_name} already exists."
        )

    customer = await customer_use_case.create(
        coach_id=str(user.id),
        username=customer_data.phone_number,
        # TODO: make it async
        password=generate_random_password(8),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name
    )

    return {
        "id": str(customer.id),
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.username,
        "last_plan_end_date": None
    }


@customer_router.get(
    "/customers",
    summary="Gets all user's customers",
    status_code=status.HTTP_200_OK)
async def get_customers(
        user_use_case: CoachUseCase = Depends(define_user_use_case),
) -> List[dict[str, Any]]:
    """
    Gets all customer for current coach

    Args:
        user_use_case: current application coach

    Returns:
        list of customers
    """
    user = user_use_case.user

    customers = []
    for customer in user.customers:
        training_plans = sorted(customer.training_plans, key=lambda x: x.end_date, reverse=True)
        customers.append({
            "id": str(customer.id),
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.username,
            "last_plan_end_date": training_plans[0].end_date.strftime("%Y-%m-%d") if training_plans else None
        })

    return customers


@customer_router.get(
    "/customers/{customer_id}",
    response_model=CustomerOut,
    status_code=status.HTTP_200_OK)
async def get_customer(
        customer_id: str,
        user_use_case: CoachUseCase = Depends(define_user_use_case),
        customer_use_case: CustomerUseCase = Depends(provide_customer_use_case)
) -> dict:
    """
    Gets specific customer by ID.

    Args:
        customer_id: str(UUID) of specified customer.
        user_use_case: service for interacting with profile
        customer_use_case: service for interacting with customer

    Raise:
        HTTPException: 400 when passed is not correct UUID as customer_id.
        HTTPException: 404 when customer not found.
        HTTPException: 400 when specified customer does not belong to the current coach.
    """
    if not await validate_uuid(customer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passed customer_id is not correct UUID value"
        )

    customer = await customer_use_case.find(filters={"id": customer_id})

    if str(customer.coach_id) != str(user_use_case.user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The client belong to another coach"
        )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )

    training_plans = sorted(customer.training_plans, key=lambda x: x.end_date, reverse=True)
    return {
        "id": str(customer.id),
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.username,
        "last_plan_end_date": training_plans[0].end_date.strftime('%Y-%m-%d') if training_plans else None
    }


@customer_router.post(
    "/customers/{customer_id}/training_plans",
    summary="Create new training plan for customer",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingPlanOut)
async def create_training_plan(
        training_plan_data: TrainingPlanIn,
        customer_id: str,
        user_use_case: CoachUseCase = Depends(define_user_use_case),
        training_plan_use_case: TrainingPlanUseCase = Depends(provide_training_plan_use_case)
) -> dict:
    """
    Creates new training plan for specified customer

    Args:
        training_plan_data: data from application user to create new training plan
        customer_id: customer's str(UUID)
        user_use_case: service for interacting with profile
        training_plan_use_case: service for interacting with customer training plans
    """
    training_plan = await training_plan_use_case.create_training_plan(
        customer_id=customer_id,
        data=training_plan_data
    )

    if training_plan:
        return {
            "id": str(training_plan.id),
            "start_date": training_plan.start_date.strftime("%Y-%m-%d"),
            "end_date": training_plan.end_date.strftime("%Y-%m-%d"),
            "number_of_trainings": len(training_plan.trainings),
            "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
            "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
            "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets])
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400,
            detail=f"Unknown error during training plan creation"
        )


@customer_router.get(
    "/customers/{customer_id}/training_plans",
    summary="Returns all training plans for customer",
    status_code=status.HTTP_200_OK)
async def get_all_training_plans(
        customer_id: str,
        user_use_case: CoachUseCase = Depends(define_user_use_case),
        customer_use_case: CustomerUseCase = Depends(provide_customer_use_case)
) -> Union[list[dict], list[None]]:
    """
    Returns all training plans for specific customer
    Endpoint can be used by both the coach and the customer

    Args:
        customer_id: customer's str(UUID)
        user_use_case: service for interacting with profile
        customer_use_case: service for interacting with customer
    """
    customer = await customer_use_case.find({"id": customer_id})
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"customer with id={customer_id} doesn't exist"
        )

    # TODO: получить через сервис GymInstructor
    training_plans = customer.training_plans

    response = []
    for training_plan in training_plans:
        response.append({
            "id": str(training_plan.id),
            "start_date": training_plan.start_date.strftime("%Y-%m-%d"),
            "end_date": training_plan.end_date.strftime("%Y-%m-%d"),
            "number_of_trainings": len(training_plan.trainings),
            "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
            "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
            "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets])
        })

    return response


@customer_router.get(
    "/customers/{customer_id}/training_plans/{training_plan_id}",
    response_model=TrainingPlanOutFull,
    status_code=status.HTTP_200_OK)
async def get_training_plan(
        training_plan_id: str,
        customer_id: str,
        user_use_case: CoachUseCase = Depends(define_user_use_case),
        training_plan_use_case: TrainingPlanUseCase = Depends(provide_training_plan_use_case),
        customer_use_case: CustomerUseCase = Depends(provide_customer_use_case)
) -> dict:
    """
    Gets full info for specific training plan by their ID
    Endpoint can be used by both the coach and the customer

    Args:
        training_plan_id: str(UUID) of specified training plan
        customer_id: str(UUID) of specified customer
        user_use_case: service for interacting with profile
        training_plan_use_case: service for interacting with customer training plans
        customer_use_case: service for interacting with customer

    Raise:
        HTTPException: 404 when customer or training plan are not found
    """
    customer = await customer_use_case.find({"id": customer_id})
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with id={customer_id} doesn't exist"
        )

    training_plan = await training_plan_use_case.find_training_plan({"id": training_plan_id})
    if training_plan is None:
        raise HTTPException(
            status_code=404,
            detail=f"Training plan with id={training_plan_id} doesn't exist"
        )

    return {
        "id": str(training_plan.id),
        "start_date": training_plan.start_date.strftime("%Y-%m-%d"),
        "end_date": training_plan.end_date.strftime("%Y-%m-%d"),
        "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
        "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
        "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets]),
        "trainings": training_plan.trainings,
        "set_rest": training_plan.set_rest,
        "exercise_rest": training_plan.exercise_rest,
        "notes": training_plan.notes
    }
