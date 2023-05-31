import uuid
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src import (
    Customer,
    TrainingPlan,
    Diet,
    DietOnTrainingPlan,
    Training,
    ExercisesOnTraining,
    Coach
)
from src.auth.dependencies import get_current_user
from src.customer.dependencies import get_coach_or_customer
from src.customer.router import customer_router
from src.customer.schemas import (
    CustomerOut,
    CustomerCreateIn,
    TrainingPlanOut,
    TrainingPlanIn,
    TrainingPlanOutFull
)
from src.customer.utils import generate_random_password
from src.dependencies import get_db
from src.utils import validate_uuid

coach_router = APIRouter()


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
            Customer.username == customer_data.phone_number
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
        username=customer_data.phone_number,
        password=generate_random_password(8),
        coach_id=str(current_user.id)
    )

    # TODO: send sms invite to customer
    # if customer.username:
    #     send_sms()

    database.add(customer)
    database.commit()

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
        current_user: Session = Depends(get_current_user)
) -> list[Optional[dict]]:
    """
    Gets all customer for current user

    Args:
        current_user: returns current application user

    Returns:
        list of customers
    """
    customers = []

    for customer in current_user.customers:
        training_plans = sorted(customer.training_plans,
                                key=lambda x: x.end_date, reverse=True)
        if training_plans:
            last_plan_end_date = training_plans[0].end_date.strftime(
                '%Y-%m-%d')
        else:
            last_plan_end_date = None

        customers.append({
            "id": str(customer.id),
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.username,
            "last_plan_end_date": last_plan_end_date
        })

    return customers


@customer_router.get(
    "/customers/{customer_id}",
    response_model=CustomerOut,
    status_code=status.HTTP_200_OK)
async def get_customer(
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)
) -> dict:
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

    if str(customer.coach_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The client belong to another coach"
        )

    training_plans = sorted(customer.training_plans,
                            key=lambda x: x.end_date, reverse=True)
    if training_plans:
        last_plan_end_date = training_plans[0].end_date.strftime('%Y-%m-%d')
    else:
        last_plan_end_date = None

    return {
        "id": str(customer.id),
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone_number": customer.username,
        "last_plan_end_date": last_plan_end_date
    }


@customer_router.post(
    "/customers/{customer_id}/training_plans",
    summary="Create new training plan for customer",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingPlanOut)
async def create_training_plan(
        training_plan_data: TrainingPlanIn,
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> dict:
    """
    Creates new training plan for specific customer

    Args:
        training_plan_data: data from application user to create new training plan
        customer_id: customer's str(UUID)
        database: dependency injection for access to database
        current_user: dependency injection to define a current user
    """
    try:
        # create training plan
        training_plan = TrainingPlan(
            start_date=training_plan_data.start_date,
            end_date=training_plan_data.end_date,
            customer_id=customer_id,
            set_rest=training_plan_data.set_rest,
            exercise_rest=training_plan_data.exercise_rest,
            notes=training_plan_data.notes
        )
        database.add(training_plan)
        database.flush()

        # create diets
        for diet_item in training_plan_data.diets:
            diet = Diet(
                proteins=diet_item.proteins,
                fats=diet_item.fats,
                carbs=diet_item.carbs
            )
            database.add(diet)
            database.flush()

            # bound diet with training_plan
            diet_on_training_plan = DietOnTrainingPlan(
                diet_id=str(diet.id),
                training_plan_id=str(training_plan.id)
            )
            database.add(diet_on_training_plan)

        # create trainings
        for training_item in training_plan_data.trainings:
            training = Training(
                name=training_item.name,
                training_plan_id=str(training_plan.id)
            )
            database.add(training)
            database.flush()

            # create exercises on training
            superset_dict = {}
            ordering = 0
            for exercise_item in training_item.exercises:
                if isinstance(exercise_item.supersets, list) and len(exercise_item.supersets) > 0:
                    if str(exercise_item.id) not in superset_dict:
                        superset_id = str(uuid.uuid4())

                        superset_dict[str(exercise_item.id)] = superset_id
                        for e in exercise_item.supersets:
                            superset_dict[str(e)] = superset_id

                exercise_on_training = ExercisesOnTraining(
                    training_id=str(training.id),
                    exercise_id=str(exercise_item.id),
                    sets=exercise_item.sets,
                    superset_id=superset_dict.get(str(exercise_item.id)),
                    ordering=ordering
                )
                database.add(exercise_on_training)
                database.flush()
                ordering += 1

        database.commit()
        database.refresh(training_plan)

    except Exception as e:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during training plan creation: {e}"
        )

    return {
        "id": str(training_plan.id),
        "start_date": training_plan.start_date.strftime('%Y-%m-%d'),
        "end_date": training_plan.end_date.strftime('%Y-%m-%d'),
        "number_of_trainings": len(training_plan.trainings),
        "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
        "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
        "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets])
    }


@customer_router.get(
    "/customers/{customer_id}/training_plans",
    summary="Returns all training plans for customer",
    status_code=status.HTTP_200_OK)
async def get_all_training_plans(
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Union[Coach, Customer] = Depends(get_coach_or_customer)
) -> Union[list[dict], list[None]]:
    """
    Returns all training plans for specific customer
    Endpoint can be used by both the coach and the customer

    Args:
        customer_id: customer's str(UUID)
        database: dependency injection for access to database
        current_user: dependency injection to define a current user
    """
    customer = database.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"customer with id={customer_id} doesn't exist"
        )

    training_plans = database.query(TrainingPlan).filter(
        TrainingPlan.customer_id == customer_id
    ).order_by(TrainingPlan.end_date.desc())

    response = []
    for training_plan in training_plans:
        response.append({
            "id": str(training_plan.id),
            "start_date": training_plan.start_date.strftime('%Y-%m-%d'),
            "end_date": training_plan.end_date.strftime('%Y-%m-%d'),
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
    database: Session = Depends(get_db),
    current_user: Union[Coach, Customer] = Depends(get_coach_or_customer)
) -> dict:
    """
    Gets specific training plan by ID
    Endpoint can be used by both the coach and the customer

    Args:
        training_plan_id: str(UUID) of specified training plan
        customer_id: str(UUID) of specified customer
        database: dependency injection for access to database
        current_user: returns current application user

    Raise:
        HTTPException: 404 when customer or training plan are not found
    """
    customer = database.query(Customer).get(customer_id)
    training_plan = database.query(TrainingPlan).get(training_plan_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"customer with id={customer_id} doesn't exist"
        )

    if not training_plan:
        raise HTTPException(
            status_code=404,
            detail=f"training plan with id={training_plan_id} doesn't exist"
        )

    trainings = []
    for training in training_plan.trainings:
        training_data = {
            "id": str(training.id),
            "name": training.name,
            "number_of_exercises": len(training.exercises)
        }

        exercises = []
        for exercise in training.exercises:
            exercise_data = {
                "id": str(exercise.id),
                "name": exercise.name
            }

            exercise_on_training = database.query(ExercisesOnTraining).filter(
                ExercisesOnTraining.training_id == str(training.id),
                ExercisesOnTraining.exercise_id == str(exercise.id)
            ).first()
            if exercise_on_training:
                exercise_data["sets"] = exercise_on_training.sets
                exercise_data["superset_id"] = exercise_on_training.superset_id
                exercise_data["ordering"] = exercise_on_training.ordering or 0
                exercises.append(exercise_data)

        exercises.sort(key=lambda x: x["ordering"])
        training_data["exercises"] = exercises

        trainings.append(training_data)

    return {
        "id": str(training_plan.id),
        "start_date": training_plan.start_date.strftime('%Y-%m-%d'),
        "end_date": training_plan.end_date.strftime('%Y-%m-%d'),
        "proteins": "/".join([str(diet.proteins) for diet in training_plan.diets]),
        "fats": "/".join([str(diet.fats) for diet in training_plan.diets]),
        "carbs": "/".join([str(diet.carbs) for diet in training_plan.diets]),
        "trainings": trainings,
        "set_rest": training_plan.set_rest,
        "exercise_rest": training_plan.exercise_rest,
        "notes": training_plan.notes
    }
