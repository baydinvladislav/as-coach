import uuid
from datetime import datetime
from typing import Union, Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session, selectinload
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
from src.core.services.coach import CoachService
from src.core.services.customer import CustomerService
from src.infrastructure.controllers.customer import customer_router
from src.infrastructure.schemas.customer import (
    CustomerOut,
    CustomerCreateIn,
    TrainingPlanOut,
    TrainingPlanIn,
    TrainingPlanOutFull
)
from src.customer.utils import generate_random_password
from src.dependencies import (
    get_db,
    get_current_user,
    provide_customer_service,
    provide_user_service
)
from src.utils import validate_uuid

coach_router = APIRouter()


@customer_router.post(
    "/customers",
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerOut)
async def create_customer(
        customer_data: CustomerCreateIn,
        user_service: CoachService = Depends(provide_user_service),
        customer_service: CustomerService = Depends(provide_customer_service)
) -> dict:
    """
    Creates new customer for coach

    Args:
        customer_data: data to create new customer
        user_service: service for interacting with profile
        customer_service: service for interacting with customer
    Raises:
        400 in case if customer with the phone number already created
        400 in case if couple last name and first name already exist
    Returns:
        dictionary with just created customer
        id, first_name, last_name and phone_number are keys
    """
    user = user_service.user

    customer_in_db = await customer_service.find({"username": customer_data.phone_number})
    if customer_data.phone_number and customer_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer {customer_in_db.first_name} {customer_in_db.last_name} "
                   f"with this phone number already exists."
        )

    customer_in_db = await customer_service.find(
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

    customer = await customer_service.create(
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
        user_service: CoachService = Depends(provide_user_service),
) -> List[dict[str, Any]]:
    """
    Gets all customer for current coach

    Args:
        user_service: current application coach

    Returns:
        list of customers
    """
    user = user_service.user

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
        user_service: CoachService = Depends(provide_user_service),
        customer_service: CustomerService = Depends(provide_customer_service)
) -> dict:
    """
    Gets specific customer by ID.

    Args:
        customer_id: str(UUID) of specified customer.
        user_service: service for interacting with profile
        customer_service: service for interacting with customer

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

    customer = await customer_service.find(filters={"id": customer_id})

    if str(customer.coach_id) != str(user_service.user.id):
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
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_coach)) -> dict:
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
            start_date=datetime.strptime(training_plan_data.start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(training_plan_data.end_date, '%Y-%m-%d').date(),
            customer_id=customer_id,
            set_rest=training_plan_data.set_rest,
            exercise_rest=training_plan_data.exercise_rest,
            notes=training_plan_data.notes
        )
        database.add(training_plan)
        await database.flush()

        # create diets
        for diet_item in training_plan_data.diets:
            diet = Diet(
                proteins=diet_item.proteins,
                fats=diet_item.fats,
                carbs=diet_item.carbs
            )
            database.add(diet)
            await database.flush()

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
            await database.flush()

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
                await database.flush()
                ordering += 1

        await database.commit()
        await database.refresh(training_plan)

    except Exception as e:
        await database.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error during training plan creation: {e}"
        )

    training_plan_in_db = await database.execute(
        select(TrainingPlan).where(TrainingPlan.id == training_plan.id).order_by().options(
            selectinload(TrainingPlan.customer),
            selectinload(TrainingPlan.diets),
            selectinload(TrainingPlan.trainings)
        )
    )
    training_plan_in_db = training_plan_in_db.scalar()

    return {
        "id": str(training_plan_in_db.id),
        "start_date": training_plan_in_db.start_date.strftime('%Y-%m-%d'),
        "end_date": training_plan_in_db.end_date.strftime('%Y-%m-%d'),
        "number_of_trainings": len(training_plan_in_db.trainings),
        "proteins": "/".join([str(diet.proteins) for diet in training_plan_in_db.diets]),
        "fats": "/".join([str(diet.fats) for diet in training_plan_in_db.diets]),
        "carbs": "/".join([str(diet.carbs) for diet in training_plan_in_db.diets])
    }


@customer_router.get(
    "/customers/{customer_id}/training_plans",
    summary="Returns all training plans for customer",
    status_code=status.HTTP_200_OK)
async def get_all_training_plans(
        customer_id: str,
        database: Session = Depends(get_db),
        current_user: Union[Coach, Customer] = Depends(get_current_user)
) -> Union[list[dict], list[None]]:
    """
    Returns all training plans for specific customer
    Endpoint can be used by both the coach and the customer

    Args:
        customer_id: customer's str(UUID)
        database: dependency injection for access to database
        current_user: dependency injection to define a current user
    """
    customer = await database.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = customer.scalar()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"customer with id={customer_id} doesn't exist"
        )

    training_plans = await database.execute(
        select(TrainingPlan).where(
            TrainingPlan.customer_id == customer_id
        ).options(
            selectinload(TrainingPlan.trainings),
            selectinload(TrainingPlan.diets),
        ).order_by(
            desc(TrainingPlan.end_date)
        )
    )

    response = []
    for training_plan in training_plans.scalars():
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
    current_user: Union[Coach, Customer] = Depends(get_current_user)
) -> dict:
    """
    Gets full info for specific training plan by their ID
    Endpoint can be used by both the coach and the customer

    Args:
        training_plan_id: str(UUID) of specified training plan
        customer_id: str(UUID) of specified customer
        database: dependency injection for access to database
        current_user: returns current application user

    Raise:
        HTTPException: 404 when customer or training plan are not found
    """

    customer = await database.execute(
        select(Customer).where(Customer.id == customer_id)
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"customer with id={customer_id} doesn't exist"
        )

    training_plan = await database.execute(
        select(TrainingPlan).where(
            TrainingPlan.id == training_plan_id
        ).options(
            selectinload(TrainingPlan.trainings)
        )
    )

    if not training_plan:
        raise HTTPException(
            status_code=404,
            detail=f"training plan with id={training_plan_id} doesn't exist"
        )

    trainings = []
    training_plan = training_plan.scalar()
    for training in training_plan.trainings:
        training_in_db = await database.execute(
            select(Training).where(
                Training.id == str(training.id)
            ).options(
                selectinload(Training.exercises)
            )
        )
        training_in_db = training_in_db.scalar()

        training_data = {
            "id": str(training_in_db.id),
            "name": training_in_db.name,
            "number_of_exercises": len(training_in_db.exercises)
        }

        exercises = []
        for exercise in training_in_db.exercises:
            exercise_data = {
                "id": str(exercise.id),
                "name": exercise.name
            }

            exercise_on_training = await database.execute(
                select(ExercisesOnTraining).where(
                    ExercisesOnTraining.training_id == str(training.id),
                    ExercisesOnTraining.exercise_id == str(exercise.id)
                )
            )
            exercise_on_training = exercise_on_training.scalar()
            if exercise_on_training:
                exercise_data["sets"] = exercise_on_training.sets
                exercise_data["superset_id"] = exercise_on_training.superset_id
                exercise_data["ordering"] = exercise_on_training.ordering or 0
                exercises.append(exercise_data)

        exercises.sort(key=lambda x: x["ordering"])
        training_data["exercises"] = exercises

        trainings.append(training_data)

    training_plan_in_db = await database.execute(
        select(TrainingPlan).where(
            TrainingPlan.id == str(training_plan.id)
        ).options(
            selectinload(TrainingPlan.diets),
            selectinload(TrainingPlan.trainings)
        )
    )

    training_plan_in_db = training_plan_in_db.scalar()
    return {
        "id": str(training_plan.id),
        "start_date": training_plan.start_date.strftime('%Y-%m-%d'),
        "end_date": training_plan.end_date.strftime('%Y-%m-%d'),
        "proteins": "/".join([str(diet.proteins) for diet in training_plan_in_db.diets]),
        "fats": "/".join([str(diet.fats) for diet in training_plan_in_db.diets]),
        "carbs": "/".join([str(diet.carbs) for diet in training_plan_in_db.diets]),
        "trainings": trainings,
        "set_rest": training_plan.set_rest,
        "exercise_rest": training_plan.exercise_rest,
        "notes": training_plan.notes
    }
